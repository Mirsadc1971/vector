# Vector Building Services

Professional commercial cleaning and building maintenance services website for Chicago and suburbs.

## 🚀 Deployment on Netlify

This site is configured for automatic deployment on Netlify.

### Quick Deploy

1. **Connect GitHub to Netlify:**
   - Go to [Netlify](https://app.netlify.com)
   - Click "Add new site" → "Import an existing project"
   - Choose "Deploy with GitHub"
   - Select the repository: `Mirsadc1971/vector`

2. **Configure Build Settings:**
   - **Build command:** `npm run build`
   - **Publish directory:** `dist`
   - **Node version:** 18 (auto-configured in netlify.toml)

3. **Deploy:**
   - Click "Deploy site"
   - Netlify will automatically build and deploy

### Environment Settings

All build settings are pre-configured in `netlify.toml`:
- Build command
- Publish directory
- Node version
- Security headers
- Caching rules

### Automatic Deployments

Once connected, Netlify will automatically deploy when:
- You push to the `master` branch
- You merge a pull request

### Domain Setup

After deployment:
1. Go to Site settings → Domain management
2. Add custom domain: `vectorbuildingservices.com`
3. Configure DNS settings as instructed by Netlify

## 🛠️ Local Development

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## 📁 Project Structure

```
/
├── src/
│   ├── layouts/         # Page layouts
│   ├── pages/           # All website pages
│   │   ├── commercial-office-cleaning-downtown-chicago/
│   │   ├── medical-facility-cleaning-glenview/
│   │   ├── restaurant-cleaning-services-naperville/
│   │   ├── retail-store-janitorial-northbrook/
│   │   ├── warehouse-floor-care-schaumburg/
│   │   └── ...
│   └── data/           # Service and location data
├── public/             # Static assets
├── astro.config.mjs    # Astro configuration
├── tailwind.config.mjs # Tailwind CSS configuration
└── netlify.toml        # Netlify deployment configuration
```

## 🏗️ Built With

- **[Astro](https://astro.build)** - Static site generator
- **[Tailwind CSS](https://tailwindcss.com)** - Utility-first CSS framework
- **Reverse Silo Architecture** - SEO-optimized structure

## 📱 Features

- Mobile-responsive design
- SEO-optimized with Schema.org markup
- Reverse silo architecture for better rankings
- Fast static site generation
- Industry-specific service pages
- Location-based targeting

## 🔧 Configuration

- **Site URL:** Configure in `astro.config.mjs`
- **Colors/Theme:** Edit in `tailwind.config.mjs`
- **Services:** Update in `src/data/services.json`
- **Locations:** Update in `src/data/locations.json`

## 📞 Contact

Vector Building Services Inc.
1400 Patriot Boulevard 2042
Glenview, IL 60026
Phone: (312) 522-5355
Email: service@vectorbuildingservices.com