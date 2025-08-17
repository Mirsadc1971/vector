<?php
/**
 * Stellar Forms - Backend Handler
 * Processes form submissions and sends email notifications
 */

// Configuration
define('ADMIN_EMAIL', 'admin@stellarpropertygroup.com');
define('FROM_EMAIL', 'noreply@stellarpropertygroup.com');
define('SITE_NAME', 'Stellar Property Group');

// CORS headers (adjust for your domain)
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');
header('Content-Type: application/json');

// Handle preflight requests
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    exit(0);
}

// Only accept POST requests
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Method not allowed']);
    exit;
}

// Get JSON input
$input = json_decode(file_get_contents('php://input'), true);

if (!$input) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'Invalid input']);
    exit;
}

// Validate form type
$formType = $input['formType'] ?? '';
if (!in_array($formType, ['contact', 'lead'])) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'Invalid form type']);
    exit;
}

// Process based on form type
try {
    if ($formType === 'contact') {
        $result = processContactForm($input);
    } else {
        $result = processLeadForm($input);
    }
    
    echo json_encode($result);
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(['success' => false, 'message' => 'Server error: ' . $e->getMessage()]);
}

/**
 * Process contact form submission
 */
function processContactForm($data) {
    // Validate required fields
    $required = ['firstName', 'lastName', 'email', 'subject', 'message'];
    foreach ($required as $field) {
        if (empty($data[$field])) {
            return ['success' => false, 'message' => "Missing required field: $field"];
        }
    }
    
    // Validate email
    if (!filter_var($data['email'], FILTER_VALIDATE_EMAIL)) {
        return ['success' => false, 'message' => 'Invalid email address'];
    }
    
    // Sanitize inputs
    $firstName = htmlspecialchars($data['firstName']);
    $lastName = htmlspecialchars($data['lastName']);
    $email = htmlspecialchars($data['email']);
    $phone = htmlspecialchars($data['phone'] ?? '');
    $subject = htmlspecialchars($data['subject']);
    $message = htmlspecialchars($data['message']);
    $newsletter = isset($data['newsletter']) ? 'Yes' : 'No';
    
    // Create email content
    $emailSubject = "New Contact Form Submission - $subject";
    $emailBody = "
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; }
            .container { max-width: 600px; margin: 0 auto; padding: 20px; }
            .header { background: #667eea; color: white; padding: 20px; text-align: center; }
            .content { background: #f5f5f5; padding: 20px; }
            .field { margin-bottom: 15px; }
            .label { font-weight: bold; color: #333; }
            .value { color: #666; }
        </style>
    </head>
    <body>
        <div class='container'>
            <div class='header'>
                <h2>New Contact Form Submission</h2>
            </div>
            <div class='content'>
                <div class='field'>
                    <div class='label'>Name:</div>
                    <div class='value'>$firstName $lastName</div>
                </div>
                <div class='field'>
                    <div class='label'>Email:</div>
                    <div class='value'>$email</div>
                </div>
                <div class='field'>
                    <div class='label'>Phone:</div>
                    <div class='value'>$phone</div>
                </div>
                <div class='field'>
                    <div class='label'>Subject:</div>
                    <div class='value'>$subject</div>
                </div>
                <div class='field'>
                    <div class='label'>Message:</div>
                    <div class='value'>$message</div>
                </div>
                <div class='field'>
                    <div class='label'>Newsletter Subscription:</div>
                    <div class='value'>$newsletter</div>
                </div>
                <div class='field'>
                    <div class='label'>Submitted:</div>
                    <div class='value'>" . date('Y-m-d H:i:s') . "</div>
                </div>
            </div>
        </div>
    </body>
    </html>
    ";
    
    // Send email
    $sent = sendEmail(ADMIN_EMAIL, $emailSubject, $emailBody, $email);
    
    // Send auto-reply
    if ($sent) {
        $autoReplySubject = "Thank you for contacting " . SITE_NAME;
        $autoReplyBody = "
        <html>
        <body>
            <p>Dear $firstName,</p>
            <p>Thank you for contacting us. We have received your message and will respond within 24 hours.</p>
            <p>Your message details:</p>
            <ul>
                <li>Subject: $subject</li>
                <li>Message: $message</li>
            </ul>
            <p>Best regards,<br>" . SITE_NAME . " Team</p>
        </body>
        </html>
        ";
        sendEmail($email, $autoReplySubject, $autoReplyBody);
    }
    
    // Store in database (optional)
    storeSubmission('contact', $data);
    
    return ['success' => $sent, 'message' => $sent ? 'Message sent successfully' : 'Failed to send message'];
}

/**
 * Process lead form submission
 */
function processLeadForm($data) {
    // Validate required fields
    $required = ['leadName', 'leadEmail', 'companySize'];
    foreach ($required as $field) {
        if (empty($data[$field])) {
            return ['success' => false, 'message' => "Missing required field: $field"];
        }
    }
    
    // Validate email
    if (!filter_var($data['leadEmail'], FILTER_VALIDATE_EMAIL)) {
        return ['success' => false, 'message' => 'Invalid email address'];
    }
    
    // Sanitize inputs
    $name = htmlspecialchars($data['leadName']);
    $email = htmlspecialchars($data['leadEmail']);
    $company = htmlspecialchars($data['company'] ?? '');
    $companySize = htmlspecialchars($data['companySize']);
    $budget = htmlspecialchars($data['budget'] ?? '');
    $timeline = htmlspecialchars($data['timeline'] ?? '');
    $needs = htmlspecialchars($data['needs'] ?? '');
    
    // Calculate lead score
    $leadScore = calculateLeadScore($data);
    
    // Create email content
    $emailSubject = "🔥 New Lead - Score: $leadScore/100";
    $emailBody = "
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; }
            .container { max-width: 600px; margin: 0 auto; padding: 20px; }
            .header { background: #667eea; color: white; padding: 20px; text-align: center; }
            .score { font-size: 24px; font-weight: bold; margin: 10px 0; }
            .content { background: #f5f5f5; padding: 20px; }
            .field { margin-bottom: 15px; }
            .label { font-weight: bold; color: #333; }
            .value { color: #666; }
            .high-priority { background: #ffeb3b; padding: 10px; margin: 10px 0; }
        </style>
    </head>
    <body>
        <div class='container'>
            <div class='header'>
                <h2>New Lead Generated</h2>
                <div class='score'>Lead Score: $leadScore/100</div>
            </div>
            " . ($leadScore >= 70 ? "<div class='high-priority'>⚡ HIGH PRIORITY LEAD - Respond immediately!</div>" : "") . "
            <div class='content'>
                <div class='field'>
                    <div class='label'>Name:</div>
                    <div class='value'>$name</div>
                </div>
                <div class='field'>
                    <div class='label'>Email:</div>
                    <div class='value'>$email</div>
                </div>
                <div class='field'>
                    <div class='label'>Company:</div>
                    <div class='value'>$company</div>
                </div>
                <div class='field'>
                    <div class='label'>Company Size:</div>
                    <div class='value'>$companySize</div>
                </div>
                <div class='field'>
                    <div class='label'>Budget:</div>
                    <div class='value'>$budget</div>
                </div>
                <div class='field'>
                    <div class='label'>Timeline:</div>
                    <div class='value'>$timeline</div>
                </div>
                <div class='field'>
                    <div class='label'>Needs:</div>
                    <div class='value'>$needs</div>
                </div>
                <div class='field'>
                    <div class='label'>Submitted:</div>
                    <div class='value'>" . date('Y-m-d H:i:s') . "</div>
                </div>
            </div>
        </div>
    </body>
    </html>
    ";
    
    // Send email with high priority if lead score is high
    $headers = '';
    if ($leadScore >= 70) {
        $headers = "X-Priority: 1\r\nImportance: High\r\n";
    }
    
    $sent = sendEmail(ADMIN_EMAIL, $emailSubject, $emailBody, $email, $headers);
    
    // Send auto-reply
    if ($sent) {
        $autoReplySubject = "Welcome to " . SITE_NAME . " - Next Steps";
        $autoReplyBody = "
        <html>
        <body>
            <p>Hi $name,</p>
            <p>Thank you for your interest in " . SITE_NAME . "!</p>
            <p>We've received your information and one of our specialists will contact you within the next 24 hours to discuss your needs.</p>
            <p>In the meantime, feel free to:</p>
            <ul>
                <li>Browse our services</li>
                <li>Check out our case studies</li>
                <li>Follow us on social media</li>
            </ul>
            <p>Looking forward to working with you!</p>
            <p>Best regards,<br>" . SITE_NAME . " Team</p>
        </body>
        </html>
        ";
        sendEmail($email, $autoReplySubject, $autoReplyBody);
    }
    
    // Store in database
    storeSubmission('lead', $data, $leadScore);
    
    // Add to CRM (if integrated)
    // addToCRM($data, $leadScore);
    
    return ['success' => $sent, 'message' => $sent ? 'Thank you! We\'ll be in touch soon.' : 'Failed to submit form'];
}

/**
 * Calculate lead score based on form data
 */
function calculateLeadScore($data) {
    $score = 0;
    
    // Company size scoring
    $sizeScores = [
        '1-10' => 10,
        '11-50' => 20,
        '51-200' => 30,
        '201-500' => 40,
        '500+' => 50
    ];
    $score += $sizeScores[$data['companySize']] ?? 0;
    
    // Budget scoring
    $budgetScores = [
        '<1k' => 5,
        '1k-5k' => 10,
        '5k-10k' => 15,
        '10k-25k' => 20,
        '25k+' => 25
    ];
    $score += $budgetScores[$data['budget']] ?? 0;
    
    // Timeline scoring
    $timelineScores = [
        'immediate' => 25,
        '1month' => 20,
        '3months' => 15,
        '6months' => 10,
        'planning' => 5
    ];
    $score += $timelineScores[$data['timeline']] ?? 0;
    
    // Has company name
    if (!empty($data['company'])) {
        $score += 10;
    }
    
    // Has detailed needs
    if (!empty($data['needs']) && strlen($data['needs']) > 50) {
        $score += 10;
    }
    
    return min($score, 100);
}

/**
 * Send email
 */
function sendEmail($to, $subject, $body, $replyTo = '', $additionalHeaders = '') {
    $headers = "MIME-Version: 1.0\r\n";
    $headers .= "Content-type: text/html; charset=UTF-8\r\n";
    $headers .= "From: " . SITE_NAME . " <" . FROM_EMAIL . ">\r\n";
    
    if ($replyTo) {
        $headers .= "Reply-To: $replyTo\r\n";
    }
    
    if ($additionalHeaders) {
        $headers .= $additionalHeaders;
    }
    
    return mail($to, $subject, $body, $headers);
}

/**
 * Store submission in database
 */
function storeSubmission($type, $data, $leadScore = null) {
    // Connect to database
    // $db = new PDO('mysql:host=localhost;dbname=stellar', 'username', 'password');
    
    // Example SQL
    /*
    $sql = "INSERT INTO form_submissions (type, data, lead_score, ip_address, created_at) 
            VALUES (:type, :data, :lead_score, :ip, NOW())";
    
    $stmt = $db->prepare($sql);
    $stmt->execute([
        'type' => $type,
        'data' => json_encode($data),
        'lead_score' => $leadScore,
        'ip' => $_SERVER['REMOTE_ADDR'] ?? ''
    ]);
    */
    
    // For now, log to file
    $logFile = 'submissions.log';
    $logData = [
        'type' => $type,
        'data' => $data,
        'lead_score' => $leadScore,
        'ip' => $_SERVER['REMOTE_ADDR'] ?? '',
        'timestamp' => date('Y-m-d H:i:s')
    ];
    
    file_put_contents($logFile, json_encode($logData) . "\n", FILE_APPEND | LOCK_EX);
}

?>