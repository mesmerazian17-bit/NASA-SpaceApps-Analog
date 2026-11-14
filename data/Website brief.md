WEBSITE DEVELOPMENT BRIEF
PLANETARY ANALOG — MISSION CONTROL SYSTEM
1. PROJECT OVERVIEW
Build a fully functional, interactive aerospace Mission Control website for a planetary analog
site selection and evaluation project.
The platform is designed to help users identify, explore, evaluate, and compare terrestrial
environments that may serve as analog sites for future lunar and Martian exploration
missions.
The system should combine:
• Scientific data visualization.
• Interactive geographic exploration.
• Engineering risk assessment.
• Environmental comparison.
• Cinematic aerospace presentation.
The website should feel like a scientific planetary exploration operations center, not a
generic business dashboard.
Important: This is an independent scientific project. Do not present it as an official NASA
product or imply NASA endorsement.
2. DESIGN DIRECTION
Core aesthetic
NASA-inspired scientific interface with a cinematic presentation layer.
Visual characteristics:
• Scientific and technical.
• Professional aerospace atmosphere.
• Dark, high-contrast interface.
• Cinematic planetary imagery.
• Precise data visualization.
• Minimal unnecessary decoration.
• Clear information hierarchy.
The design should balance two characteristics:
1. CINEMATIC EXPERIENCE
Large-scale planetary imagery, immersive transitions, atmospheric backgrounds, and
a strong opening experience.
2. SCIENTIFIC OPERATIONS INTERFACE
Precise coordinates, technical metadata, charts, filters, mission parameters, and
engineering information.
Avoid:
• Generic SaaS dashboard appearance.
• Excessive neon colors.
• Cyberpunk styling.
• Decorative elements that reduce readability.
• Excessive glassmorphism.
• Oversized typography inside technical panels.
Color palette
Primary background:
• Deep space navy: #080D16
• Secondary navy: #101A29
• Panel background: #121E2D
Primary accent:
• Scientific cyan: #52D6E8
• Mission gold: #E7B85C
Supporting colors:
• Slate gray: #8091A5
• White: #E8EEF5
• Warning orange: #F2A65A
• Critical red: #E66A6A
Marker semantics:
• Gold: Primary site match.
• Cyan: Composite partner site.
• Slate: NASA validation benchmark, only when such a benchmark exists in the
provided data.
Typography
Use:
• Modern sans-serif for headings and general interface text.
• Monospaced fonts for coordinates, telemetry, IDs, and technical measurements.
Typography should be clean, compact, and highly readable.
3. WEBSITE EXPERIENCE AND STRUCTURE
Use a HYBRID CINEMATIC DASHBOARD structure.
The experience consists of two main layers.
A. CINEMATIC ENTRY EXPERIENCE
Create an introductory landing experience before the main dashboard.
Elements:
• Full-screen planetary landscape imagery.
• Project title: PLANETARY ANALOG.
• Subtitle: MISSION CONTROL SYSTEM.
• Short project description.
• Primary CTA: ENTER MISSION CONTROL.
• Subtle atmospheric motion and scientific visual elements.
The opening screen should establish the atmosphere of planetary exploration.
Keep animations smooth and restrained. Prioritize performance.
When the user clicks ENTER MISSION CONTROL, transition into the operational dashboard.
B. MAIN MISSION CONTROL DASHBOARD
The dashboard should occupy the available desktop viewport.
Use a three-column layout:
LEFT: MISSION CONTROLS
CENTER: INTERACTIVE MAP
RIGHT: ENGINEERING ANALYSIS
The interface should prioritize information density without becoming visually overwhelming.
4. LEFT PANEL — MISSION CONTROLS
Create a technical control panel containing:
Planetary target selection
Dropdown options:
• Lunar South Pole
• Jezero Crater
• Arsia Lava Tube
Failure mode selection
Support multiple selections:
• electrostatic_dust
• low_angle_shadow_navigation
• gps_denied_subsurface_slam
• subsurface_core_drilling
Display readable labels rather than raw identifiers.
Composite two-site mode
Allow users to enable or disable a composite campaign involving two analog sites.
When enabled, display the selected primary site and potential partner site.
Operational filters
Include:
• Exclude protected national parks.
• Maximum road distance slider.
All filters must affect the actual available dataset where the relevant fields exist.
Do not invent filter behavior if the dataset lacks the required information. Explain missing
data or request clarification.
5. CENTER PANEL — INTERACTIVE GEOGRAPHIC MAP
This is the primary visual focus of the dashboard.
Use React Leaflet or MapLibre.
Requirements:
• Interactive geographic map.
• Zoom and pan.
• Location markers based on actual dataset coordinates.
• Distinct marker colors based on site roles.
• Selected marker highlighting.
• Location information popup or side detail.
• Smooth map movement when a site is selected.
When a user selects a site, use the map library's fly-to functionality to move toward its
coordinates.
Seasonal operational window
Display relevant seasonal or environmental timing information when available in the dataset.
Do not generate fictional seasonal values.
Imagery comparison drawer
Create a collapsible bottom drawer containing an imagery comparison experience.
Compare:
• Earth satellite imagery of the selected analog location.
• Relevant lunar or Martian orbital imagery.
Use actual imagery sources or clearly identified illustrative imagery.
Keep the imagery comparison visually distinct from the geographic map.
6. RIGHT PANEL — ENGINEERING ANALYSIS
Engineering risk radar chart
Use Recharts to create a five-axis radar chart.
The five axes should represent the engineering dimensions supported by the actual dataset.
Possible dimensions include:
• Terrain similarity.
• Geological similarity.
• Illumination conditions.
• Dust/environmental conditions.
• Accessibility.
Important: These are proposed dimensions, not assumed dataset fields. Inspect the actual
dataset and map the available metrics appropriately.
Physics delta alert
Create a high-contrast scientific warning panel explaining important physical differences
between Earth analog environments and their target planetary environments.
Include the following reference values when relevant:
• Earth gravity: approximately 1g.
• Moon gravity: approximately 0.16g.
Also explain that Earth's atmosphere, pressure, temperature, and environmental conditions
differ significantly from lunar and Martian conditions.
Do not imply that a terrestrial analog perfectly reproduces an extraterrestrial environment.
AI-generated readiness brief
Display an engineering readiness summary based on available site information and analysis.
The brief should identify:
• Relevant advantages.
• Environmental limitations.
• Potential engineering challenges.
• Important uncertainties.
• Recommended areas for further testing.
Clearly distinguish data-backed findings from generated interpretation.
Hardware subsystem test scores
Display subsystem scores only when supported by the dataset or a documented scoring
method.
Do not invent scores or label arbitrary values as validated engineering measurements.
7. DATA INTEGRATION
Primary dataset:
earth_candidates.json
seed_locations.json
Before implementing the dashboard:
1. Inspect the complete JSON structure.
2. Identify all available fields and nested objects.
3. Identify data types and relationships.
4. Determine which fields correspond to geographic coordinates, site scores,
environmental measurements, and engineering metrics.
5. Explain the proposed mapping between dataset fields and frontend components.
Use the actual dataset as the source of truth.
Requirements:
• Do not hardcode data already present in JSON.
• Do not fabricate missing values.
• Do not assume field names without inspecting the file.
• Build reusable data transformation and filtering functions.
• Include loading, empty, and error states.
• Keep the interface functional even when some optional fields are unavailable.
If additional data is needed, identify it explicitly instead of silently creating placeholder
scientific results.
8. VISUAL ASSET INTEGRATION
Use the supplied OpenArt assets.
Expected asset categories:
• Mars landscape.
• Lunar South Pole terrain.
• Planetary orbital imagery.
• Geological terrain imagery.
• Rover or exploration equipment.
• Optional cinematic atmospheric background.
Use these assets selectively.
Do not use generated imagery as a substitute for actual geographic coordinates, scientific
measurements, or interactive map data.
Create a centralized asset structure so images can be replaced easily.
Suggested asset directory:
public/
images/
mars-landscape.png
lunar-south-pole.png
orbital-earth.png
planetary-orbit.png
rover.png
mission-background.png
Adjust filenames to match the actual files supplied.
9. TECHNOLOGY STACK
Use:
• Next.js App Router.
• React.
• TypeScript.
• Tailwind CSS.
• Lucide React.
• Recharts.
• React Leaflet or MapLibre.
Keep the project modular.
Suggested structure:
app/
page.tsx
mission-control/
page.tsx
components/
landing/
dashboard/
mission-controls/
map/
engineering/
charts/
lib/
data/
filters/
calculations/
public/
data/
images/
Use client components only where necessary for interactive functionality.
10. RESPONSIVENESS AND PERFORMANCE
Primary target: desktop and laptop.
Requirements:
• Full viewport dashboard.
• Three-column desktop layout.
• Readable technical information.
• Scrollable panels when content exceeds available height.
• Responsive tablet and mobile fallback.
• Smooth but restrained transitions.
• Optimized image loading.
• Avoid unnecessary heavy 3D effects.
Do not sacrifice scientific readability for visual effects.
11. DEVELOPMENT WORKFLOW
Do not immediately generate the entire application without inspecting the provided
resources.
Follow these stages:
STAGE 1 — RESOURCE INSPECTION
• Read the website brief.
• Inspect all supplied assets.
• Inspect the actual JSON dataset.
• Explain the available data and missing information.
STAGE 2 — ARCHITECTURE
• Propose component structure.
• Explain how the dataset will connect to the interface.
• Identify dependencies and potential technical limitations.
STAGE 3 — VISUAL IMPLEMENTATION
• Build the cinematic entry experience.
• Build the three-column dashboard.
• Integrate the supplied images.
STAGE 4 — DATA INTEGRATION
• Connect the actual JSON.
• Implement filters and selection logic.
• Connect map markers and engineering charts.
STAGE 5 — TESTING
• Check data loading.
• Check filtering.
• Check map interactions.
• Check chart updates.
• Check missing data handling.
• Check responsive behavior.
12. EXPECTED FINAL RESULT
Deliver a working, editable, data-driven Mission Control website.
The final product must not merely resemble a screenshot.
Its map, filters, charts, and site information must function using the actual supplied data.
Keep the source code understandable, organized, and maintainable for a beginner
developer.
Before beginning implementation, report your understanding of the resources and identify
any missing requirements.