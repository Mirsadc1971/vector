const fs = require('fs');

// Read the current file
let content = fs.readFileSync('src/pages/locations/suburbs/index.astro', 'utf-8');

// Remove the old intro and tailored solutions sections
content = content.replace(/  <!-- Intro Section -->[\s\S]*?<!-- Tailored Solutions -->[\s\S]*?<\/section>\n\n/, '');

// Replace Areas We Serve section with card layout
const oldAreas = `  <!-- Areas We Serve -->
  <section class="py-16">
    <div class="container mx-auto px-4">
      <div class="max-w-5xl mx-auto">
        <h2 class="text-3xl font-bold mb-6">Areas We Serve</h2>

        <p class="text-lg text-gray-700 mb-8">
          We provide building services across many suburbs, including:
        </p>

        <div class="grid md:grid-cols-2 gap-8 mb-8">
          {serviceAreas.map(area => (
            <div class="bg-white border border-gray-200 p-6 rounded-lg">
              <h3 class="font-bold text-xl mb-4 text-primary-600">{area.region}:</h3>
              <div class="flex flex-wrap gap-2">
                {area.cities.map((city, index) => (
                  <>
                    <a href={city.link} class="text-primary-600 hover:underline">
                      {city.name}
                    </a>
                    {index < area.cities.length - 1 && <span class="text-gray-400">•</span>}
                  </>
                ))}
              </div>
            </div>
          ))}
        </div>

        <p class="text-sm text-gray-600 italic">
          (Each of these locations should link to its own dedicated page for SEO.)
        </p>
      </div>
    </div>
  </section>`;

const newAreas = `  <!-- Areas We Serve -->
  <section class="py-16">
    <div class="container mx-auto px-4">
      <div class="max-w-7xl mx-auto">
        <h2 class="text-3xl font-bold mb-6 text-center">Areas We Serve</h2>
        <p class="text-lg text-gray-700 mb-12 text-center max-w-3xl mx-auto">
          Professional HOA & condominium property services across Chicagoland's suburbs. Click any location to learn more about our services in your area.
        </p>

        <!-- North Shore (7 cards) -->
        <div class="mb-12">
          <h3 class="text-2xl font-bold mb-6 text-primary-600">North Shore</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 mb-8">
            <a href="evanston" class="group bg-white border border-gray-200 p-6 rounded-lg hover:shadow-lg hover:border-primary-300 transition-all duration-300">
              <h4 class="font-bold text-lg text-gray-900 group-hover:text-primary-600 mb-2">Evanston</h4>
              <p class="text-gray-600 text-sm">HOA & condo services in Evanston's vibrant lakefront community</p>
            </a>
            <a href="wilmette" class="group bg-white border border-gray-200 p-6 rounded-lg hover:shadow-lg hover:border-primary-300 transition-all duration-300">
              <h4 class="font-bold text-lg text-gray-900 group-hover:text-primary-600 mb-2">Wilmette</h4>
              <p class="text-gray-600 text-sm">Expert property services for Wilmette's historic North Shore community</p>
            </a>
            <a href="winnetka" class="group bg-white border border-gray-200 p-6 rounded-lg hover:shadow-lg hover:border-primary-300 transition-all duration-300">
              <h4 class="font-bold text-lg text-gray-900 group-hover:text-primary-600 mb-2">Winnetka</h4>
              <p class="text-gray-600 text-sm">Comprehensive services for Winnetka's luxury communities</p>
            </a>
            <a href="kenilworth" class="group bg-white border border-gray-200 p-6 rounded-lg hover:shadow-lg hover:border-primary-300 transition-all duration-300">
              <h4 class="font-bold text-lg text-gray-900 group-hover:text-primary-600 mb-2">Kenilworth</h4>
              <p class="text-gray-600 text-sm">Professional services for Kenilworth's exclusive associations</p>
            </a>
            <a href="glencoe" class="group bg-white border border-gray-200 p-6 rounded-lg hover:shadow-lg hover:border-primary-300 transition-all duration-300">
              <h4 class="font-bold text-lg text-gray-900 group-hover:text-primary-600 mb-2">Glencoe</h4>
              <p class="text-gray-600 text-sm">Property care for Glencoe's wooded neighborhoods</p>
            </a>
            <a href="highland-park" class="group bg-white border border-gray-200 p-6 rounded-lg hover:shadow-lg hover:border-primary-300 transition-all duration-300">
              <h4 class="font-bold text-lg text-gray-900 group-hover:text-primary-600 mb-2">Highland Park</h4>
              <p class="text-gray-600 text-sm">HOA & condo services for Highland Park's large communities</p>
            </a>
            <a href="lake-forest" class="group bg-white border border-gray-200 p-6 rounded-lg hover:shadow-lg hover:border-primary-300 transition-all duration-300">
              <h4 class="font-bold text-lg text-gray-900 group-hover:text-primary-600 mb-2">Lake Forest</h4>
              <p class="text-gray-600 text-sm">Reliable property services for Lake Forest's suburban communities</p>
            </a>
          </div>
        </div>

        <!-- Northwest Suburbs (6 cards) -->
        <div class="mb-12">
          <h3 class="text-2xl font-bold mb-6 text-primary-600">Northwest Suburbs</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
            <a href="glenview" class="group bg-white border border-gray-200 p-6 rounded-lg hover:shadow-lg hover:border-primary-300 transition-all duration-300">
              <h4 class="font-bold text-lg text-gray-900 group-hover:text-primary-600 mb-2">Glenview</h4>
              <p class="text-gray-600 text-sm">Trusted property services for Glenview's suburban associations</p>
            </a>
            <a href="northbrook" class="group bg-white border border-gray-200 p-6 rounded-lg hover:shadow-lg hover:border-primary-300 transition-all duration-300">
              <h4 class="font-bold text-lg text-gray-900 group-hover:text-primary-600 mb-2">Northbrook</h4>
              <p class="text-gray-600 text-sm">HOA & condo services in Northbrook's established neighborhoods</p>
            </a>
            <a href="deerfield" class="group bg-white border border-gray-200 p-6 rounded-lg hover:shadow-lg hover:border-primary-300 transition-all duration-300">
              <h4 class="font-bold text-lg text-gray-900 group-hover:text-primary-600 mb-2">Deerfield</h4>
              <p class="text-gray-600 text-sm">Expert maintenance & landscaping for Deerfield communities</p>
            </a>
            <a href="buffalo-grove" class="group bg-white border border-gray-200 p-6 rounded-lg hover:shadow-lg hover:border-primary-300 transition-all duration-300">
              <h4 class="font-bold text-lg text-gray-900 group-hover:text-primary-600 mb-2">Buffalo Grove</h4>
              <p class="text-gray-600 text-sm">Professional services for Buffalo Grove's large residential campuses</p>
            </a>
            <a href="wheeling" class="group bg-white border border-gray-200 p-6 rounded-lg hover:shadow-lg hover:border-primary-300 transition-all duration-300">
              <h4 class="font-bold text-lg text-gray-900 group-hover:text-primary-600 mb-2">Wheeling</h4>
              <p class="text-gray-600 text-sm">Reliable property care for Wheeling's condo complexes</p>
            </a>
            <a href="lincolnshire" class="group bg-white border border-gray-200 p-6 rounded-lg hover:shadow-lg hover:border-primary-300 transition-all duration-300">
              <h4 class="font-bold text-lg text-gray-900 group-hover:text-primary-600 mb-2">Lincolnshire</h4>
              <p class="text-gray-600 text-sm">HOA & condo services for Lincolnshire's residential neighborhoods</p>
            </a>
          </div>
        </div>

        <!-- Farther Suburbs (4 cards) -->
        <div class="mb-12">
          <h3 class="text-2xl font-bold mb-6 text-primary-600">Farther Suburbs</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <a href="libertyville" class="group bg-white border border-gray-200 p-6 rounded-lg hover:shadow-lg hover:border-primary-300 transition-all duration-300">
              <h4 class="font-bold text-lg text-gray-900 group-hover:text-primary-600 mb-2">Libertyville</h4>
              <p class="text-gray-600 text-sm">Property services for Libertyville's growing residential communities</p>
            </a>
            <a href="vernon-hills" class="group bg-white border border-gray-200 p-6 rounded-lg hover:shadow-lg hover:border-primary-300 transition-all duration-300">
              <h4 class="font-bold text-lg text-gray-900 group-hover:text-primary-600 mb-2">Vernon Hills</h4>
              <p class="text-gray-600 text-sm">Comprehensive services for Vernon Hills' residential communities</p>
            </a>
            <a href="lake-zurich" class="group bg-white border border-gray-200 p-6 rounded-lg hover:shadow-lg hover:border-primary-300 transition-all duration-300">
              <h4 class="font-bold text-lg text-gray-900 group-hover:text-primary-600 mb-2">Lake Zurich</h4>
              <p class="text-gray-600 text-sm">Property services for Lake Zurich's lakefront associations</p>
            </a>
            <a href="barrington" class="group bg-white border border-gray-200 p-6 rounded-lg hover:shadow-lg hover:border-primary-300 transition-all duration-300">
              <h4 class="font-bold text-lg text-gray-900 group-hover:text-primary-600 mb-2">Barrington</h4>
              <p class="text-gray-600 text-sm">Professional services for Barrington's townhome developments</p>
            </a>
          </div>
        </div>
      </div>
    </div>
  </section>`;

// Replace the old areas section
content = content.replace(oldAreas, newAreas);

// Save the file
fs.writeFileSync('src/pages/locations/suburbs/index.astro', content);

console.log('Successfully updated suburbs index page with 17 card layout!');