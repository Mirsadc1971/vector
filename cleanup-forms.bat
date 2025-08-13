@echo off
echo ========================================
echo Manage369 Forms Cleanup Script
echo ========================================
echo.

REM Backup current forms.html
echo Step 1: Backing up current forms.html...
copy forms.html forms-BACKUP-%date:~-4%%date:~4,2%%date:~7,2%.html
echo Backup created: forms-BACKUP-%date:~-4%%date:~4,2%%date:~7,2%.html
echo.

REM Replace with clean version
echo Step 2: Replacing with clean forms page...
copy forms-clean.html forms.html /Y
echo forms.html has been replaced with working version
echo.

REM Delete unused form files
echo Step 3: Removing unused form files...
if exist consultation_form.html (
    del consultation_form.html
    echo Deleted: consultation_form.html
)
if exist fix_contact_forms.py (
    del fix_contact_forms.py
    echo Deleted: fix_contact_forms.py
)
if exist fix_form_placement.py (
    del fix_form_placement.py
    echo Deleted: fix_form_placement.py
)
if exist fix_form_position.py (
    del fix_form_position.py
    echo Deleted: fix_form_position.py
)
if exist remove_duplicate_forms.py (
    del remove_duplicate_forms.py
    echo Deleted: remove_duplicate_forms.py
)
echo.

echo ========================================
echo Cleanup Complete!
echo ========================================
echo.
echo The following changes were made:
echo 1. Backed up old forms.html
echo 2. Replaced with working forms (2 forms only)
echo 3. Removed unused form files
echo.
echo Your forms page now has:
echo - Property Management Inquiry Form
echo - Maintenance Request Form
echo.
echo All forms send to: service@manage369.com
echo.
pause