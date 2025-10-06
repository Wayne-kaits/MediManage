# GitHub Upload Guide for MediManage

This guide will help you upload the MediManage web application to GitHub.

## Prerequisites

- Git installed on your computer
- GitHub account created
- Repository prepared (this has been done)

## Step 1: Create a New Repository on GitHub

1. Go to [GitHub](https://github.com)
2. Click the **+** icon in the top right corner
3. Select **New repository**
4. Fill in the details:
   - **Repository name:** `medimanage` (or your preferred name)
   - **Description:** "A comprehensive web-based Hospital Management System built with Flask"
   - **Visibility:** Choose Public or Private
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
5. Click **Create repository**

## Step 2: Prepare Your Local Repository

The repository has already been prepared with:
- ✅ Updated `.gitignore` (excludes Replit, Zencoder, desktop apps, and multi-tenant files)
- ✅ Clean README.md for single-tenant version
- ✅ LICENSE file (MIT License)
- ✅ .gitattributes for proper line endings
- ✅ CONTRIBUTING.md for contributors

## Step 3: Review What Will Be Uploaded

### Files that WILL be included:
- Core application files: `app.py`, `main.py`, `models.py`, `routes.py`, `forms.py`, `db.py`, `utils.py`
- Templates: All HTML files in `templates/` (except `templates/multitenant/`)
- Static files: CSS, JavaScript, images in `static/`
- Configuration: `requirements.txt`
- Documentation: `README.md`, `LICENSE`, `CONTRIBUTING.md`

### Files that will NOT be included (filtered by .gitignore):
- ❌ `.zencoder/` - Zencoder configuration
- ❌ `.replit` - Replit configuration
- ❌ `WindowsDesktopApp/` - Desktop application
- ❌ `ElectronApp/` - Electron application
- ❌ Multi-tenant files: `app_multitenant.py`, `routes_multitenant.py`, etc.
- ❌ Test files: `test_*.py`
- ❌ Database files: `*.db`, `*.sqlite`
- ❌ Python cache: `__pycache__/`, `*.pyc`
- ❌ Build artifacts: `build/`, `dist/`
- ❌ Extra documentation files
- ❌ Log files: `*.log`

## Step 4: Stage and Commit Your Changes

Open PowerShell or Command Prompt and run:

```powershell
# Navigate to your project directory
cd "d:\Softwares\MediManage"

# Check current status
git status

# Add all files (respecting .gitignore)
git add .

# Commit the changes
git commit -m "Initial commit: Single-tenant Hospital Management System"
```

## Step 5: Connect to GitHub Repository

After creating your repository on GitHub, you'll see a page with commands. Use these:

```powershell
# Add the remote repository (replace YOUR_USERNAME and YOUR_REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Verify the remote was added
git remote -v

# Push to GitHub
git push -u origin main
```

**Note:** If your default branch is `master` instead of `main`, use:
```powershell
git push -u origin master
```

## Step 6: Verify Upload

1. Go to your GitHub repository page
2. Verify all files are uploaded correctly
3. Check that the README.md displays properly
4. Ensure sensitive files are NOT visible (databases, logs, etc.)

## Step 7: Configure Repository Settings (Optional)

### Add Topics
1. Go to your repository on GitHub
2. Click the gear icon next to "About"
3. Add topics: `flask`, `python`, `hospital-management`, `healthcare`, `medical`, `web-application`

### Add Description
Add a short description: "A comprehensive web-based Hospital Management System built with Flask"

### Enable Issues
1. Go to Settings → Features
2. Enable Issues for bug reports and feature requests

### Add Repository Website
If you deploy the application, add the URL in the repository settings

## Troubleshooting

### Issue: "remote origin already exists"
```powershell
# Remove existing remote
git remote remove origin

# Add the correct remote
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
```

### Issue: Authentication failed
- Use a Personal Access Token instead of password
- Go to GitHub Settings → Developer settings → Personal access tokens
- Generate a new token with `repo` scope
- Use the token as your password when pushing

### Issue: Large files rejected
- Check if any large files are being tracked
- Add them to .gitignore
- Remove from Git cache: `git rm --cached filename`

### Issue: Wrong files uploaded
```powershell
# Check what will be committed
git status

# Remove files from staging
git reset HEAD filename

# Update .gitignore and try again
```

## Post-Upload Checklist

- [ ] Repository is created on GitHub
- [ ] All necessary files are uploaded
- [ ] Sensitive files are NOT uploaded (check .gitignore)
- [ ] README.md displays correctly
- [ ] LICENSE file is present
- [ ] Repository description and topics are added
- [ ] Issues are enabled
- [ ] Repository visibility is set correctly (Public/Private)

## Next Steps

After uploading to GitHub, you can:

1. **Share your repository** - Send the GitHub URL to others
2. **Enable GitHub Pages** - Host documentation
3. **Set up CI/CD** - Automate testing and deployment
4. **Add badges** - Show build status, coverage, etc.
5. **Create releases** - Tag versions of your application
6. **Accept contributions** - Review and merge pull requests

## Quick Command Reference

```powershell
# Check status
git status

# Add all changes
git add .

# Commit changes
git commit -m "Your commit message"

# Push to GitHub
git push origin main

# Pull latest changes
git pull origin main

# View commit history
git log --oneline

# Create a new branch
git checkout -b feature-name

# Switch branches
git checkout main
```

## Need Help?

- GitHub Documentation: https://docs.github.com
- Git Documentation: https://git-scm.com/doc
- Create an issue in the repository for specific questions

---

**Ready to upload? Follow the steps above and your MediManage application will be on GitHub!** 🚀