# PowerShell script to replace footers in all property management files

$oldFooter = @"
<!-- PERFECT FOOTER HTML - EXACT SPECIFICATIONS -->
<!-- Footer -->
<footer class="site-footer">
<div class="footer-content">
<!-- Company Info Column -->
<div class="footer-column">
<h3>Manage369</h3>
<p>1400 Patriot Boulevard 357<br/>Glenview, IL 60026</p>
<p style="margin-top: 10px; color: #4b5563; font-weight: 500;">IDFPR Management Firm License 291.000211</p>
<p style="margin-top: 10px;"><strong>Phone:</strong> <a href="tel:8476522338">(847) 652-2338</a><br/>
<strong>Email:</strong> <a href="mailto:service@manage369.com">service@manage369.com</a></p>
</div>
<!-- Quick Links Column -->
<div class="footer-column">
<h3>Quick Links</h3>
<ul>
<li><a href="../../property-management/">Areas We Serve</a></li>
<li><a href="../../blog/">Blog</a></li>
<li><a href="../../contact.html">Contact</a></li>
<li><a href="../../payment-methods.html">Payment Methods</a></li>
<li><a href="../../services.html">Services</a></li></ul>
</div>
<!-- Resources Column -->
<div class="footer-column">
<h3>Resources</h3>
<ul>
<li><a href="../../accessibility.html">Accessibility</a></li>
<li><a href="../../forms.html">Forms &amp; Documents</a></li>
<li><a href="../../legal-disclaimers.html">Legal Disclaimers</a></li>
<li><a href="../../privacy-policy.html">Privacy Policy</a></li>
<li><a href="../../sitemap.html">Sitemap</a></li>
<li><a href="../../terms-of-service.html">Terms of Service</a></li></ul>
</div>
</div>
<div class="footer-bottom">
<div style="text-align: center; margin-bottom: 10px; color: #4b5563; font-size: 0.9rem;">
                CAI National Member | IREM Certified | CCIM Designated | NAR Member | IDFPR Licensed
            </div>
<p style="text-align: center; color: #4b5563;">© 2025 Manage369. All rights reserved.</p>
</div>
</footer>
"@

$newFooter = @"
<!-- Footer -->
<footer style="background: #2C3E50; color: #e5e7eb; padding: 1.5rem 0; margin-top: 2rem;">
    <div style="max-width: 1200px; margin: 0 auto; padding: 0 2rem;">
        <div style="display: grid; grid-template-columns: 2fr 1fr 1fr 1fr 1.5fr; gap: 2rem; align-items: start;">
            <!-- Company Info -->
            <div>
                <h3 style="font-size: 1.1rem; margin: 0 0 0.3rem 0; color: #F1C40F; font-weight: 600;">MANAGE369</h3>
                <p style="font-size: 0.85rem; margin: 0; line-height: 1.3; color: #e5e7eb;">
                    1400 Patriot Blvd #357, Glenview, IL<br>
                    📱 Text: <a href="sms:8476522338" style="color: #60a5fa; text-decoration: none;">(847) 652-2338</a><br>
                    <a href="mailto:service@manage369.com" style="color: #60a5fa; text-decoration: none;">service@manage369.com</a><br>
                    <span style="font-size: 0.8rem; color: #9ca3af;">License: 291.000211</span>
                </p>
            </div>
            
            <!-- Services -->
            <div>
                <h4 style="font-size: 0.9rem; margin: 0 0 0.3rem 0; color: #F1C40F; font-weight: 600;">Services</h4>
                <div style="font-size: 0.8rem; line-height: 1.3;">
                    <a href="/services/condominium-management/" style="color: #e5e7eb; text-decoration: none; display: block; padding: 2px 0;">Condominium</a>
                    <a href="/services/hoa-management/" style="color: #e5e7eb; text-decoration: none; display: block; padding: 2px 0;">HOA</a>
                    <a href="/services/townhome-management/" style="color: #e5e7eb; text-decoration: none; display: block; padding: 2px 0;">Townhome</a>
                    <a href="/services/financial-management/" style="color: #e5e7eb; text-decoration: none; display: block; padding: 2px 0;">Financial</a>
                    <a href="/services/maintenance-coordination/" style="color: #e5e7eb; text-decoration: none; display: block; padding: 2px 0;">Maintenance</a>
                    <a href="/services/board-support/" style="color: #e5e7eb; text-decoration: none; display: block; padding: 2px 0;">Board Support</a>
                </div>
            </div>
            
            <!-- Quick Links -->
            <div>
                <h4 style="font-size: 0.9rem; margin: 0 0 0.3rem 0; color: #F1C40F; font-weight: 600;">Quick Links</h4>
                <div style="font-size: 0.8rem; line-height: 1.3;">
                    <a href="/property-management/" style="color: #e5e7eb; text-decoration: none; display: block; padding: 2px 0;">Areas We Serve</a>
                    <a href="/contact.html" style="color: #e5e7eb; text-decoration: none; display: block; padding: 2px 0;">Contact</a>
                    <a href="/forms.html" style="color: #e5e7eb; text-decoration: none; display: block; padding: 2px 0;">Forms</a>
                    <a href="/payment-methods.html" style="color: #e5e7eb; text-decoration: none; display: block; padding: 2px 0;">Pay Dues</a>
                    <a href="/blog/" style="color: #e5e7eb; text-decoration: none; display: block; padding: 2px 0;">Blog</a>
                    <a href="/sitemap.html" style="color: #e5e7eb; text-decoration: none; display: block; padding: 2px 0;">Sitemap</a>
                </div>
            </div>
            
            <!-- Resources -->
            <div>
                <h4 style="font-size: 0.9rem; margin: 0 0 0.3rem 0; color: #F1C40F; font-weight: 600;">Resources</h4>
                <div style="font-size: 0.8rem; line-height: 1.3;">
                    <a href="/legal-disclaimers.html" style="color: #e5e7eb; text-decoration: none; display: block; padding: 2px 0;">Legal</a>
                    <a href="/privacy-policy.html" style="color: #e5e7eb; text-decoration: none; display: block; padding: 2px 0;">Privacy</a>
                    <a href="/terms-of-service.html" style="color: #e5e7eb; text-decoration: none; display: block; padding: 2px 0;">Terms</a>
                    <a href="/accessibility.html" style="color: #e5e7eb; text-decoration: none; display: block; padding: 2px 0;">Accessibility</a>
                    <a href="/leave-review.html" style="color: #e5e7eb; text-decoration: none; display: block; padding: 2px 0;">Leave Review</a>
                </div>
            </div>
            
            <!-- Certifications & Copyright -->
            <div style="text-align: right;">
                <div style="font-size: 0.75rem; color: #F1C40F; line-height: 1.4; margin-bottom: 0.5rem;">
                    CAI National Member<br>
                    IREM Certified<br>
                    CCIM Designated<br>
                    NAR Member<br>
                    IDFPR Licensed
                </div>
                <div style="font-size: 0.75rem; color: #6b7280; margin-top: 0.5rem; padding-top: 0.5rem; border-top: 1px solid #374151;">
                    © 2025 Manage369<br>
                    All rights reserved
                </div>
            </div>
        </div>
    </div>
</footer>
"@

# Get all property management files that need updating
$files = Get-ChildItem -Path "property-management" -Recurse -Filter "index.html" | Where-Object { 
    $content = Get-Content $_.FullName -Raw
    $content -notmatch "background: #2C3E50"
}

Write-Host "Found $($files.Count) files to update"

foreach ($file in $files) {
    $fullPath = $file.FullName
    Write-Host "Processing: $fullPath"
    
    $content = Get-Content $fullPath -Raw
    $newContent = $content -replace [regex]::Escape($oldFooter), $newFooter
    
    Set-Content -Path $fullPath -Value $newContent -NoNewline
    Write-Host "Updated: $fullPath"
}

Write-Host "Footer replacement complete!"