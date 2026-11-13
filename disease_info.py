"""
Disease Information and Agricultural Knowledge Base
Provides comprehensive symptoms, descriptions, safe cultural/preventive measures,
water & irrigation protocols, and AI treatment suggestions for all 10 tomato crop leaf conditions.
"""
DISEASE_DETAILS = {
    "tomato_healthy": {
        "name": "Tomato Healthy",
        "scientific_name": "Solanum lycopersicum",
        "category": "Healthy",
        "status": "Healthy",
        "badge_color": "success",
        "severity": "None",
        "accent_color": "#10b981",  # Emerald
        "summary": "Plant foliage is vigorous, well-hydrated, and completely free of pathogen lesions.",
        "description": "The leaf appears vigorous, vibrant green, and free from visible pathogenic infections or nutritional disorders. Plant cellular metabolism and photosynthesis are functioning optimally.",
        "symptoms": [
            "Uniform vibrant green leaf pigmentation without chlorosis, mottling, or yellow halos.",
            "Smooth, intact leaf surface without spots, powdery mildew, or velvety mold growth.",
            "Stems and petioles are firm, upright, well-hydrated, and structurally sound."
        ],
        "prevention": [
            "Maintain balanced watering: water strictly at the soil base, avoiding overhead wetting.",
            "Ensure 6-8 hours of direct daily sunlight and well-draining organic compost-rich soil.",
            "Apply balanced N-P-K fertilizer according to growth stages (avoid excessive nitrogen in fruiting).",
            "Maintain adequate plant spacing (18-24 inches) to foster continuous airflow."
        ],
        "immediate_action": "Continue regular cultural maintenance and conduct weekly scouting for early insect or fungal signs.",
        "water_guidance": {
            "verdict": "YES - Regular Hydration Required",
            "status": "Optimal Drip Irrigation",
            "daily_volume": "1.5 - 2.0 Liters / mature plant / day",
            "leaf_wetness_risk": "Low to Moderate (Foliage must stay dry to remain pathogen-free)",
            "method": "Direct drip irrigation or soaker hose at root zone",
            "best_timing": "Early Morning (6:00 AM - 8:00 AM)",
            "rules": [
                "Water at the soil base beneath mulch; never use overhead sprinklers.",
                "Check top 2 inches of soil: irrigate when slightly dry to the touch.",
                "Maintain 2-3 inches of organic straw mulch to retain uniform moisture.",
                "Ensure generous drainage to prevent root hypoxia or waterlogging."
            ]
        },
        "treatment_guide": {
            "urgency": "Routine Cultivation",
            "organic_options": [
                "Apply compost tea or diluted seaweed kelp drench monthly to stimulate root microflora.",
                "Incorporate beneficial mycorrhizal fungi at root zone during growth flushes."
            ],
            "chemical_options": [
                "No synthetic fungicides or bactericides required for healthy leaves.",
                "Avoid unnecessary prophylactic pesticide sprays to preserve beneficial pollinators."
            ],
            "cultural_steps": [
                "Trellis vines securely to prevent foliage from drooping onto the ground.",
                "Prune bottom suckers up to 10-12 inches to maximize air currents.",
                "Sanitize pruning equipment before each use."
            ],
            "recovery_outlook": "Plant is thriving. Yield potential remains at 100%."
        }
    },
    "tomato_bacterial_spot": {
        "name": "Tomato Bacterial Spot",
        "scientific_name": "Xanthomonas perforans / Xanthomonas vesicatoria",
        "category": "Bacterial",
        "status": "Infected",
        "badge_color": "danger",
        "severity": "High",
        "accent_color": "#ef4444",  # Crimson
        "summary": "Destructive bacterial spots that spread rapidly across wet foliage via rain-splash and overhead watering.",
        "description": "A destructive bacterial disease affecting tomato foliage, stems, and fruit. It thrives in warm, humid, and rainy weather, spreading primarily via splashing water, contaminated garden tools, and handling wet plants.",
        "symptoms": [
            "Small, dark brown to black water-soaked circular lesions (1-3 mm) across leaves.",
            "Lesions frequently display a distinctive faint yellowish chlorotic halo.",
            "Severe infections cause leaves to turn brown, dry out, become brittle, and drop prematurely.",
            "Rough, scabby, raised spots may also emerge on green and ripening fruit."
        ],
        "prevention": [
            "Avoid overhead sprinkler irrigation; always employ precision drip or soaker hose irrigation.",
            "Never handle, prune, or harvest from plants when dew or surface moisture is present.",
            "Sterilize pruning shears and tools with 70% rubbing alcohol between each individual vine.",
            "Practice a minimum 2-3 year crop rotation away from peppers, eggplants, and potatoes.",
            "Sow certified disease-free seeds and plant resistant tomato cultivars."
        ],
        "immediate_action": "Prune and immediately bag infected lower foliage. Trash or burn infected plant debris—never compost.",
        "water_guidance": {
            "verdict": "CAUTION - Restrict Foliar Water & Reduce Base Volume",
            "status": "Strict Sub-Surface Drip Only",
            "daily_volume": "1.0 - 1.2 Liters / plant (Allow surface soil to dry)",
            "leaf_wetness_risk": "EXTREME - Water droplets spread Xanthomonas bacteria across the field",
            "method": "Sub-surface root drip only (ZERO foliage contact)",
            "best_timing": "Early Morning (Allows ground surface to dry rapidly in sun)",
            "rules": [
                "NEVER use overhead sprinklers, garden hose sprayers, or misting systems.",
                "Do not touch, prune, or irrigate plants when dew or moisture is visible on leaves.",
                "Allow top 2-3 inches of soil to dry out between waterings to lower canopy humidity.",
                "Direct all water exclusively to root zone beneath plastic or straw barrier mulch."
            ]
        },
        "treatment_guide": {
            "urgency": "Immediate Action (Within 24 Hours)",
            "organic_options": [
                "Apply Copper Octanoate (copper soap) foliar spray every 7-10 days before rain.",
                "Foliar spray with Bacillus subtilis bio-fungicide to outcompete bacterial colonies.",
                "Apply potassium bicarbonate solution (3g/L) to alter leaf surface micro-pH."
            ],
            "chemical_options": [
                "Tank-mix fixed copper bactericide with Mancozeb for synergized control against copper-tolerant strains.",
                "Rotate bactericide chemical modes of action to prevent resistant bacterial populations."
            ],
            "cultural_steps": [
                "Strip infected lower foliage up to 15 inches from ground and seal in disposal bags.",
                "Apply 3 inches of clean straw mulch to stop rain-splash from soil to leaves.",
                "Clean garden shoes and equipment with 10% bleach after working in affected rows."
            ],
            "recovery_outlook": "Infected leaves will not heal, but new shoots will grow clean if foliage remains dry and protected."
        }
    },
    "tomato_early_blight": {
        "name": "Tomato Early Blight",
        "scientific_name": "Alternaria solani",
        "category": "Fungal",
        "status": "Infected",
        "badge_color": "danger",
        "severity": "Moderate to High",
        "accent_color": "#f97316",  # Amber Orange
        "summary": "Fungal target-board concentric spots attacking lower leaves and climbing upward in wet conditions.",
        "description": "A prevalent fungal infection that begins on older, lower foliage and progresses upward through the canopy. It produces distinctive brown concentric rings resembling a target board.",
        "symptoms": [
            "Dark brown to black spots with prominent concentric rings ('bullseye' appearance).",
            "Surrounding leaf tissue turns yellow (chlorosis) as fungal toxins diffuse outward.",
            "Progressive defoliation advancing from ground level up the main vine.",
            "Sunken, leathery, dark lesions developing near the stem end of fruits."
        ],
        "prevention": [
            "Mulch heavily around plant bases with straw or plastic to block soil spores from splashing.",
            "Stake or cage plants upright to keep foliage well above damp soil.",
            "Prune bottom 12 inches of foliage once plants reach 24 inches tall.",
            "Ensure wide spacing to facilitate rapid drying of leaves by wind.",
            "Rotate crops annually with non-solanaceous botanical families."
        ],
        "immediate_action": "Remove infected bottom foliage immediately and discard in sealed bags away from the garden.",
        "water_guidance": {
            "verdict": "CAUTION - Keep Foliage Bone Dry",
            "status": "Strict Ground Drip Under Mulch",
            "daily_volume": "1.0 - 1.3 Liters / plant",
            "leaf_wetness_risk": "VERY HIGH - Spores require 6-8 hours of leaf wetness to germinate",
            "method": "Buried drip line or soaker hose beneath 3-inch straw mulch",
            "best_timing": "Early morning exclusively (Sunrise to 8:00 AM)",
            "rules": [
                "Water solely at ground level; Alternaria spores splash up from wet soil.",
                "Lay down thick mulch to form an impenetrable barrier over soil spores.",
                "Never water if ambient humidity exceeds 85% or right before dusk.",
                "Prune bottom 12 inches of foliage so no leaves hover near damp soil."
            ]
        },
        "treatment_guide": {
            "urgency": "High Priority (Within 24-48 Hours)",
            "organic_options": [
                "Liquid copper fungicide or organic Bordeaux mixture applied to upper and lower leaf surfaces.",
                "Bio-fungicide containing Bacillus amyloliquefaciens or Serenade bio-protectant.",
                "Cold-pressed neem oil foliar spray (0.5%) as a biological anti-sporulant."
            ],
            "chemical_options": [
                "Chlorothalonil (Daconil) protective broad-spectrum fungicide every 7-10 days.",
                "Azoxystrobin or Pyraclostrobin (strobilurin group) rotated to halt fungal respiration."
            ],
            "cultural_steps": [
                "Strip all infected lower foliage showing concentric bullseyes and burn or landfill.",
                "Stake vines vertically and tie branches to maintain breezy open airflow.",
                "Rake and destroy fallen leaf debris from the garden floor weekly."
            ],
            "recovery_outlook": "Canopy defoliation stops once lower branches are pruned and fungicide barrier is established."
        }
    },
    "tomato_late_blight": {
        "name": "Tomato Late Blight",
        "scientific_name": "Phytophthora infestans",
        "category": "Fungal/Oomycete",
        "status": "Infected",
        "badge_color": "danger",
        "severity": "Critical",
        "accent_color": "#b91c1c",  # Dark Crimson
        "summary": "Catastrophic fast-moving water mold capable of destroying entire tomato fields in 48-72 hours.",
        "description": "An aggressive, fast-moving oomycete pathogen notorious for causing the historic Irish Potato Famine. Under cool, damp conditions, it can destroy an entire tomato crop within days.",
        "symptoms": [
            "Large, irregular, water-soaked pale green to dark brown oily lesions on leaves and stems.",
            "White, velvety downy fungal growth on the undersides of leaves in humid mornings.",
            "Rapid browning, shriveling, and catastrophic collapse of entire vines.",
            "Firm, greasy, olive-brown sunken patches covering green and ripening fruit."
        ],
        "prevention": [
            "Provide maximum sunlight exposure and full ventilation in greenhouses and open fields.",
            "Keep foliage 100% dry; avoid any field activity when leaves are damp.",
            "Eradicate volunteer tomato and potato plants nearby that harbor overwintering spores.",
            "Choose certified late-blight resistant cultivars (e.g., Defiant, Mountain Magic, Iron Lady).",
            "Monitor regional agricultural extension alerts for active late-blight spore tracking."
        ],
        "immediate_action": "Isolate the area immediately. Bag and destroy heavily infected whole plants to protect neighboring crops.",
        "water_guidance": {
            "verdict": "ALERT - Withhold Watering / Strict Root Drip Only",
            "status": "Emergency Moisture Suppression",
            "daily_volume": "0.8 - 1.0 Liters / plant (Cease non-essential watering)",
            "leaf_wetness_risk": "CRITICAL - Phytophthora zoospores swim in free moisture droplets and wipe out rows overnight",
            "method": "Strict root emitter under impermeable plastic sheeting",
            "best_timing": "Dry sunny morning only; HALT watering during rainy/foggy periods",
            "rules": [
                "Cease all watering that contributes to canopy air humidity.",
                "In greenhouses or high tunnels, run circulation fans 24/7 to drop relative humidity below 70%.",
                "Ensure rapid drainage; never allow standing water or puddles in tomato beds.",
                "Keep foliage completely dry at all times; rogue out dense weed cover."
            ]
        },
        "treatment_guide": {
            "urgency": "EMERGENCY (Immediate Response Required)",
            "organic_options": [
                "Copper hydroxide or copper sulfate preventative spray at maximum registered label rate.",
                "Potassium silicate bio-stimulant to reinforce epidermal plant cell walls."
            ],
            "chemical_options": [
                "Systemic translaminar fungicides: Mandipropamid (Revus), Cymoxanil (Curzate), or Fluopicolide.",
                "Protective tank-mixes with Chlorothalonil or Mancozeb before rainy cool fronts."
            ],
            "cultural_steps": [
                "Immediately dig up, double-bag, and landfill or incinerate severely infected plants.",
                "Never compost late-blight material—spores easily overwinter in compost piles.",
                "Notify neighboring growers if late blight is confirmed in your plot."
            ],
            "recovery_outlook": "Severe infections are irreversible. Quick rogueing saves surrounding healthy rows."
        }
    },
    "tomato_leaf_mold": {
        "name": "Tomato Leaf Mold",
        "scientific_name": "Passalora fulva (syn. Fulvia fulva)",
        "category": "Fungal",
        "status": "Infected",
        "badge_color": "warning",
        "severity": "Moderate",
        "accent_color": "#d97706",  # Amber
        "summary": "High-humidity mold causing yellow upper-leaf blotches with velvety olive-green underside spores.",
        "description": "A fungal disease predominantly found in high-tunnel structures and greenhouses where relative humidity exceeds 85% with warm daytime temperatures.",
        "symptoms": [
            "Pale green to yellowish diffuse patches on the upper surface of older leaves.",
            "Olive-green to velvety brown mold growth directly underneath on the lower leaf surface.",
            "Infected leaves eventually curl, wither, turn brittle brown, and drop.",
            "Blossoms and fruit are rarely infected directly, but defoliation stunts fruit size."
        ],
        "prevention": [
            "Increase greenhouse ventilation through ridge vents, exhaust fans, and circulation blowers.",
            "Space plants generously and prune suckers to optimize cross-canopy air movement.",
            "Maintain night temperatures warm enough to prevent condensation on leaf surfaces.",
            "Use drip irrigation exclusively to eliminate surface splashing and puddle evaporation.",
            "Select resistant cultivars with known Cf gene resistance."
        ],
        "immediate_action": "Reduce indoor humidity immediately below 80% and carefully trim moldy leaves with sanitized shears.",
        "water_guidance": {
            "verdict": "REDUCE WATERING - Dehumidify Environment",
            "status": "Controlled Sub-Surface Moisture",
            "daily_volume": "1.0 - 1.2 Liters / plant",
            "leaf_wetness_risk": "VERY HIGH - Spores require >85% relative humidity and leaf condensation",
            "method": "Buried drip tape 1-2 inches below soil",
            "best_timing": "Early Morning (Allows greenhouse air to heat up and dehumidify)",
            "rules": [
                "Run exhaust and circulation fans continuously to keep humidity below 80%.",
                "Never wet leaves; low atmospheric humidity is the ultimate cure for leaf mold.",
                "Space containers at least 2 feet apart to eliminate trapped moist air pockets.",
                "Heat greenhouse slightly before dusk to stay above the dew point and prevent condensation."
            ]
        },
        "treatment_guide": {
            "urgency": "Prompt (Within 2-3 Days)",
            "organic_options": [
                "Potassium bicarbonate (MilStop) to dissolve existing fungal spore walls on contact.",
                "Copper octanoate bio-fungicide applied every 7-10 days to protect unaffected foliage.",
                "Bio-fungicide spray containing Bacillus pumilus."
            ],
            "chemical_options": [
                "Chlorothalonil, Cyazofamid, or Difenoconazole labeled for greenhouse tomato use."
            ],
            "cultural_steps": [
                "Prune dense interior canopy suckers to open wide vertical light channels.",
                "Wash greenhouse glazing and benches with quaternary ammonium or 10% bleach between crops.",
                "Install horizontal airflow fans to ensure constant air velocity across the leaves."
            ],
            "recovery_outlook": "Lowering humidity below 80% and pruning affected foliage halts mold spread within 5-7 days."
        }
    },
    "tomato_septoria_leaf_spot": {
        "name": "Tomato Septoria Leaf Spot",
        "scientific_name": "Septoria lycopersici",
        "category": "Fungal",
        "status": "Infected",
        "badge_color": "danger",
        "severity": "Moderate to High",
        "accent_color": "#dc2626",  # Red
        "summary": "Dense tiny circular spots with grey centers and black specks, causing rapid lower defoliation.",
        "description": "A very prevalent fungal leaf disease that attacks tomato leaves throughout the growing season, typically starting after fruit set on lower leaves.",
        "symptoms": [
            "Numerous small circular spots (1-3 mm wide) with dark brown borders and grayish-white centers.",
            "Tiny black fruiting bodies (pycnidia) clearly visible inside the gray centers with a magnifying lens.",
            "Leaves turn yellow around spots, dry up, curl, and drop prematurely.",
            "Severe defoliation exposes developing green fruit to sunscald and fruit crack."
        ],
        "prevention": [
            "Apply a 2-3 inch layer of clean organic straw mulch around each plant base.",
            "Keep plant foliage dry; water early in the day so morning sun dries accidental moisture.",
            "Remove dead plant debris thoroughly at the end of every growing season.",
            "Clean and sanitize tomato stakes and cages before reusing them with a 10% bleach wash.",
            "Rotate crops on a 3-year cycle with unrelated crops (e.g., legumes or brassicas)."
        ],
        "immediate_action": "Prune spotted lower leaves at the stem and apply clean mulch to suppress splash-borne fungal spores.",
        "water_guidance": {
            "verdict": "CAUTION - Base Drip Only + Straw Mulch Shield",
            "status": "Sub-Mulch Drip Irrigation",
            "daily_volume": "1.0 - 1.4 Liters / plant",
            "leaf_wetness_risk": "VERY HIGH - Water droplets launch pycnidiospores upward like artillery onto clean foliage",
            "method": "Deep slow drip irrigation beneath 3-inch straw mulch layer",
            "best_timing": "6:00 AM - 8:00 AM only",
            "rules": [
                "Apply clean organic mulch immediately over all exposed bare soil around the vine.",
                "Zero leaf contact: keep garden hoses and cans strictly below the lowest branch.",
                "Never water on windy mornings when airborne droplets can drift into foliage.",
                "Allow top 2 inches of soil to dry out between deep waterings."
            ]
        },
        "treatment_guide": {
            "urgency": "High Priority (Within 24-48 Hours)",
            "organic_options": [
                "Liquid copper octanoate applied every 7-10 days as a protective barrier.",
                "Bio-fungicide containing Bacillus subtilis sprayed on remaining healthy leaves.",
                "Pure neem oil spray applied to leaf undersides to inhibit spore germination."
            ],
            "chemical_options": [
                "Chlorothalonil (Daconil) or Mancozeb protective treatments applied at first sign.",
                "Pyraclostrobin (Cabrio) or Boscalid (Endura) for systemic commercial suppression."
            ],
            "cultural_steps": [
                "Prune and destroy all bottom leaves exhibiting small circular spots with white centers.",
                "Disinfect cages, stakes, and twine with a 10% bleach solution before reuse.",
                "Rotate out of solanaceous crops for a minimum of 3 years."
            ],
            "recovery_outlook": "Pruning infected lower leaves and mulching stops upward progression; new leaves stay clean."
        }
    },
    "tomato_spider_mites": {
        "name": "Tomato Spider Mites",
        "scientific_name": "Tetranychus urticae (Two-Spotted Spider Mite)",
        "category": "Pest",
        "status": "Infected",
        "badge_color": "warning",
        "severity": "Moderate",
        "accent_color": "#eab308",  # Golden Yellow
        "summary": "Microscopic sap-sucking pests that produce fine golden stippling and delicate webs during hot, dry weather.",
        "description": "Microscopic arachnid pests that pierce plant cell walls to suck chlorophyll and sap. They proliferate explosively during hot, dry, dusty environmental conditions.",
        "symptoms": [
            "Fine yellow, bronze, or white stippling (tiny dots) on the upper leaf surface.",
            "Delicate silken webbing visible on leaf undersides, leaf axils, and growing tips.",
            "Leaves turn dull bronze, become brittle, dry out, and drop prematurely.",
            "Severe infestations stunt growth and can kill whole vines in hot weather."
        ],
        "prevention": [
            "Keep pathways moist or vegetated to suppress airborne dust that favors mite reproduction.",
            "Encourage natural predatory beneficials like lady beetles, lacewings, and predatory mites (Phytoseiulus persimilis).",
            "Avoid excessive synthetic nitrogen fertilizers, which produce lush tissue that attracts mites.",
            "Ensure plants receive regular, deep watering to minimize drought stress."
        ],
        "immediate_action": "Spray leaf undersides thoroughly with a strong blast of water or organic insecticidal soap / cold-pressed neem oil.",
        "water_guidance": {
            "verdict": "YES - Regular Hydration + Morning Foliar Underside Rinse",
            "status": "Hydration Balance (Mites Flourish in Drought & Dust)",
            "daily_volume": "1.8 - 2.2 Liters / plant (Drought stress triggers rapid mite breeding)",
            "leaf_wetness_risk": "LOW - Unlike fungi, spider mites hate high moisture and humidity!",
            "method": "Root hydration + forceful morning foliar water blast on leaf undersides",
            "best_timing": "Early Morning: deep root soak + underside leaf rinse",
            "rules": [
                "Drought-stressed plants are spider mite magnets; keep root zone consistently moist.",
                "Use a strong water jet on leaf undersides early in the morning to physically knock off mites and webs.",
                "Moisten adjacent garden pathways to suppress airborne dust that carries mites.",
                "Do not allow container pots to dry out completely; maintain uniform moisture."
            ]
        },
        "treatment_guide": {
            "urgency": "Prompt (Within 2-3 Days)",
            "organic_options": [
                "Cold-pressed pure Neem oil (1% solution) sprayed thoroughly on leaf undersides.",
                "Potassium salts of fatty acids (insecticidal soap) sprayed at dusk or dawn.",
                "Release biological predatory mites (Phytoseiulus persimilis or Neoseiulus californicus)."
            ],
            "chemical_options": [
                "Bifenazate (Floramite) or Abamectin miticides for severe infestations.",
                "Avoid synthetic pyrethroid insecticides which wipe out natural predators and trigger severe mite flare-ups."
            ],
            "cultural_steps": [
                "Hose down infested foliage every 2-3 days in early morning.",
                "Prune out and discard heavily webbed terminal growth tips into sealed trash bags.",
                "Cut back on excessive high-nitrogen chemical fertilizer."
            ],
            "recovery_outlook": "Mite populations plummet sharply within 4-7 days following humidity elevation and neem sprays."
        }
    },
    "tomato_target_spot": {
        "name": "Tomato Target Spot",
        "scientific_name": "Corynespora cassiicola",
        "category": "Fungal",
        "status": "Infected",
        "badge_color": "danger",
        "severity": "Moderate to High",
        "accent_color": "#ea580c",  # Deep Orange
        "summary": "Warm-weather fungal spots that enlarge with concentric target rings and tear out, causing shot-holes.",
        "description": "A fungal foliar disease common in warm, humid regions. It forms characteristic circular lesions on leaves, stems, and fruit, often confused with early blight.",
        "symptoms": [
            "Small water-soaked circular spots on leaves that enlarge up to 10-15 mm across.",
            "Light brown lesions with definite concentric circles, often with a distinct yellow halo.",
            "Lesions may tear or fall out, giving leaves a tattered or shot-hole appearance.",
            "Fruit lesions appear sunken, dark brown, and circular with crater-like cracks."
        ],
        "prevention": [
            "Provide wide row spacing and trellis vines to ensure maximum air flow.",
            "Prune lower foliage and suckers to keep plants open and dry.",
            "Avoid working in tomato fields when leaves are wet from dew or rain.",
            "Destroy weed hosts (such as wild solanaceous weeds) around the growing area.",
            "Practice strict 3-year crop rotation."
        ],
        "immediate_action": "Remove affected foliage and eliminate weeds around plant rows to improve air circulation.",
        "water_guidance": {
            "verdict": "CAUTION - Keep Canopy Dry & Space Plants",
            "status": "Root-Zone Drip Only",
            "daily_volume": "1.0 - 1.3 Liters / plant",
            "leaf_wetness_risk": "VERY HIGH - Corynespora cassiicola thrives in warm, wet foliage microclimates",
            "method": "Low-pressure drip emitter right at soil line",
            "best_timing": "Early Morning (6:00 AM - 8:00 AM)",
            "rules": [
                "Avoid any top-down irrigation or foliar splashing.",
                "Prune lower leaves and lateral suckers to keep lower plant zone dry and breezy.",
                "Water deeply and infrequently rather than shallow daily sprinklings.",
                "Ensure wide spacing between plants (at least 24 inches) to accelerate drying."
            ]
        },
        "treatment_guide": {
            "urgency": "High Priority (Within 24-48 Hours)",
            "organic_options": [
                "Copper hydroxide or copper sulfate pentahydrate sprays applied every 7 days.",
                "Bio-fungicides like Regalia (Reynoutria extract) to stimulate plant systemic acquired resistance."
            ],
            "chemical_options": [
                "Fluxapyroxad + Pyraclostrobin (Priaxor) or Boscalid fungicides.",
                "Chlorothalonil broad-spectrum protectant applied before high-humidity weather."
            ],
            "cultural_steps": [
                "Remove and destroy foliage with target-like concentric lesions.",
                "Eradicate wild solanaceous weeds around the plot boundary.",
                "Clean up all crop residues thoroughly after harvest."
            ],
            "recovery_outlook": "Canopy opening and protectant sprays prevent infection from migrating onto green fruit."
        }
    },
    "tomato_mosaic_virus": {
        "name": "Tomato Mosaic Virus (ToMV)",
        "scientific_name": "Tomato mosaic tobamovirus",
        "category": "Viral",
        "status": "Infected",
        "badge_color": "danger",
        "severity": "High",
        "accent_color": "#9333ea",  # Purple
        "summary": "Mechanically transmissible virus causing mottled light/dark green mosaic leaves and distorted shoestring foliage.",
        "description": "A highly infectious and persistent tobamovirus easily transmitted mechanically via hands, tools, clothes, and seeds. It can survive in dry plant debris and soil for years.",
        "symptoms": [
            "Mottling of leaves with alternating light green, yellow, and dark green mosaic patterns.",
            "Distorted, blistered, crinkled, or 'shoestring' (fern-like) leaf deformation.",
            "Stunted plant growth and severely reduced flowering and fruit set.",
            "Uneven fruit ripening and internal brown necrosis in tomato flesh."
        ],
        "prevention": [
            "Plant certified virus-free seed or virus-resistant varieties (labeled 'ToMV' or 'TMV').",
            "Wash hands thoroughly with soap and water before handling tomato plants.",
            "Smokers and tobacco users must wash hands thoroughly, as tobacco products can carry related viruses.",
            "Sterilize pruning shears with a 10% trisodium phosphate (TSP) or 20% nonfat milk solution.",
            "Do not save seeds from infected plants."
        ],
        "immediate_action": "Carefully dig up and bag entire infected plants and root systems. Do not compost.",
        "water_guidance": {
            "verdict": "YES - Regular Base Drip / Zero Contact During Irrigation",
            "status": "Contactless Base Drip",
            "daily_volume": "1.3 - 1.6 Liters / plant",
            "leaf_wetness_risk": "MODERATE - Mechanically transmitted via hands and hoses during watering tasks",
            "method": "Automated drip irrigation - do not drag hoses across vines",
            "best_timing": "Scheduled automated morning cycle",
            "rules": [
                "Never drag garden hoses, boots, or hands across infected plants; virus enters via microscopic leaf wounds.",
                "Irrigate via automated drip lines to avoid physical handling of foliage.",
                "Never touch healthy vines after irrigating or pruning symptomatic plants.",
                "Keep soil evenly hydrated to avoid secondary physiological stress."
            ]
        },
        "treatment_guide": {
            "urgency": "IMMEDIATE (Isolate or Rogue Within 24 Hours)",
            "organic_options": [
                "No cure exists once a plant is infected with systemic ToMV.",
                "Foliar skim milk spray (20% nonfat dry milk in water) deactivates virus particles on plant surfaces and tools."
            ],
            "chemical_options": [
                "No chemical viricides exist for plant mosaic viruses."
            ],
            "cultural_steps": [
                "Carefully dig up and incinerate or trash infected plants including roots.",
                "Wash hands thoroughly with soap and warm water; tobacco smokers must decontaminate before gardening.",
                "Sterilize tools with 10% trisodium phosphate (TSP) or 20% milk solution.",
                "Select certified virus-resistant varieties (labeled TMV / ToMV)."
            ],
            "recovery_outlook": "Systemic viral infection is permanent. Rogueing out infected vines is mandatory to save healthy plants."
        }
    },
    "tomato_yellow_leaf_curl_virus": {
        "name": "Tomato Yellow Leaf Curl Virus (TYLCV)",
        "scientific_name": "Tomato yellow leaf curl begomovirus",
        "category": "Viral",
        "status": "Infected",
        "badge_color": "danger",
        "severity": "Critical",
        "accent_color": "#c026d3",  # Fuchsia / Magenta
        "summary": "Devastating whitefly-transmitted virus causing severe upward leaf cupping, stunted bushy canopy, and flower drop.",
        "description": "A devastating viral disease transmitted by the sweetpotato whitefly (Bemisia tabaci). When infection occurs early in plant development, fruit yield loss can reach 100%.",
        "symptoms": [
            "Severe upward curling and cupping of leaf margins.",
            "Marked yellowing (chlorosis) along leaf edges and between veins.",
            "Significant reduction in leaf size, giving foliage a stunted, bunchy appearance.",
            "Bushy, stunted plant canopy with heavy blossom drop and little to no fruit set."
        ],
        "prevention": [
            "Control whitefly vectors using yellow sticky insect traps and insect exclusion netting (50-mesh).",
            "Apply organic horticultural oils or neem oil to reduce whitefly populations.",
            "Plant TYLCV-resistant or tolerant hybrid tomato varieties.",
            "Eliminate alternate weed hosts (like black nightshade and datura) near the field.",
            "Use reflective silver or aluminum mulches to repel incoming whiteflies."
        ],
        "immediate_action": "Rogue out infected plants immediately and treat surrounding plants with insecticidal soap to curb whitefly vectors.",
        "water_guidance": {
            "verdict": "YES - Standard Base Irrigation + Whitefly Vector Suppression",
            "status": "Consistent Base Irrigation",
            "daily_volume": "1.2 - 1.5 Liters / plant",
            "leaf_wetness_risk": "LOW - Spread by whitefly vectors (Bemisia tabaci), not water splash",
            "method": "Drip irrigation at base under reflective silver mulch",
            "best_timing": "Early morning",
            "rules": [
                "Maintain consistent root moisture so the stunted plant does not suffer water stress.",
                "Use reflective silver or aluminum mulch over the soil bed: it repels whiteflies while conserving soil moisture.",
                "Avoid excessive drought which weakens plant defenses against insect vectors.",
                "Drip irrigation under mulch prevents disturbing whiteflies resting on lower foliage."
            ]
        },
        "treatment_guide": {
            "urgency": "Immediate Action (Control Whitefly Vectors Now)",
            "organic_options": [
                "Deploy bright yellow sticky cards above the canopy to trap whiteflies.",
                "Spray cold-pressed Neem oil or insecticidal soap to smother whitefly nymphs and eggs.",
                "Install 50-mesh fine insect exclusion netting over beds."
            ],
            "chemical_options": [
                "Imidacloprid, Dinotefuran, or Acetamiprid systemic insecticides applied to control whitefly populations.",
                "Pyriproxyfen insect growth regulator to disrupt whitefly breeding."
            ],
            "cultural_steps": [
                "Rogue out early-infected stunted plants to remove virus reservoirs.",
                "Eliminate nearby alternate weed hosts like wild nightshade, datura, and mallow.",
                "Plant TYLCV-resistant hybrid tomato cultivars (e.g., Tygress, Skyway, Red Snapper)."
            ],
            "recovery_outlook": "Infected plants remain stunted and will not produce marketable yield; vector suppression is essential."
        }
    }
}


def normalize_class_key(class_name: str) -> str:
    """
    Normalizes arbitrary class folder or label names into a standardized dictionary key.
    Examples:
        'Tomato___Bacterial_spot' -> 'tomato_bacterial_spot'
        'Tomato_Early_Blight' -> 'tomato_early_blight'
        'Tomato Healthy' -> 'tomato_healthy'
        'Tomato___Spider_mites_Two-spotted_spider_mite' -> 'tomato_spider_mites'
    """
    if not class_name:
        return "tomato_healthy"

    raw = str(class_name).strip().lower()
    raw = raw.replace("___", "_").replace("__", "_")
    raw = raw.replace(" ", "_").replace("-", "_")

    if "healthy" in raw:
        return "tomato_healthy"
    if "bacterial" in raw or ("spot" in raw and "bacterial" in raw):
        return "tomato_bacterial_spot"
    if "early" in raw and "blight" in raw:
        return "tomato_early_blight"
    if "late" in raw and "blight" in raw:
        return "tomato_late_blight"
    if "leaf_mold" in raw or "mold" in raw:
        return "tomato_leaf_mold"
    if "septoria" in raw:
        return "tomato_septoria_leaf_spot"
    if "spider" in raw or "mite" in raw:
        return "tomato_spider_mites"
    if "target" in raw:
        return "tomato_target_spot"
    if "mosaic" in raw:
        return "tomato_mosaic_virus"
    if "yellow" in raw or "curl" in raw:
        return "tomato_yellow_leaf_curl_virus"

    if raw in DISEASE_DETAILS:
        return raw

    if not raw.startswith("tomato_"):
        candidate = f"tomato_{raw}"
        if candidate in DISEASE_DETAILS:
            return candidate

    return raw


def get_disease_info(class_name: str) -> dict:
    """
    Retrieves full agricultural information dictionary for any given class name.
    Guarantees backward compatibility with existing keys while supplying all enriched data.
    """
    key = normalize_class_key(class_name)
    if key in DISEASE_DETAILS:
        return DISEASE_DETAILS[key]

    # Clean fallback for unexpected classes
    display_title = class_name.replace("___", " - ").replace("_", " ").title()
    is_healthy = "healthy" in class_name.lower()
    return {
        "name": display_title,
        "scientific_name": "Solanum lycopersicum",
        "category": "Healthy" if is_healthy else "Disease",
        "status": "Healthy" if is_healthy else "Infected",
        "badge_color": "success" if is_healthy else "warning",
        "severity": "None" if is_healthy else "Moderate",
        "accent_color": "#10b981" if is_healthy else "#f59e0b",
        "summary": f"Identified condition: {display_title}.",
        "description": f"Condition identified as {display_title}. Consult an agricultural specialist for localized diagnostics.",
        "symptoms": [
            f"Foliar abnormalities corresponding to {display_title}.",
            "Observe leaf pigmentation, surface texture, and vigor closely."
        ],
        "prevention": [
            "Maintain proper plant spacing and sanitation.",
            "Water at the base using drip irrigation to avoid wet foliage.",
            "Prune lower infected leaves and avoid working when plants are wet.",
            "Practice annual crop rotation with non-solanaceous crops."
        ],
        "immediate_action": "Isolate the plant and monitor progress after pruning any damaged leaves.",
        "water_guidance": {
            "verdict": "CAUTION - Base Watering Only",
            "status": "Standard Base Drip",
            "daily_volume": "1.2 - 1.5 Liters / plant",
            "leaf_wetness_risk": "Moderate",
            "method": "Direct ground root drip only",
            "best_timing": "Early Morning",
            "rules": [
                "Avoid wetting foliage.",
                "Ensure adequate soil drainage.",
                "Water early in the day."
            ]
        },
        "treatment_guide": {
            "urgency": "Prompt Review",
            "organic_options": ["Apply neem oil or copper soap bio-fungicide."],
            "chemical_options": ["Consult local extension service for approved regional compounds."],
            "cultural_steps": ["Prune damaged lower leaves and space plants."],
            "recovery_outlook": "Monitor new foliage flushes for clean growth."
        }
    }


def build_field_precautions(disease_key: str, confidence: float, reviewer_eta: str = "in the next field visit") -> list[str]:
    """
    Generates practical precaution steps for the grower until a plant specialist or reviewer arrives.
    The output is written in a natural, AI agronomist voice for dashboard display.
    """
    info = get_disease_info(disease_key)
    status = info.get("status", "Infected")
    water_guidance = info.get("water_guidance", {})
    prevention = info.get("prevention", [])
    immediate_action = info.get("immediate_action", "Inspect the affected plants immediately.")

    steps = []
    if status == "Healthy":
        steps.append("I recommend continuing routine monitoring and keeping the irrigation schedule consistent.")
        steps.append("Please check the canopy daily for early signs of stress, yellowing, or unusual leaf spotting.")
        steps.append("Maintain drip irrigation and avoid wetting the leaves during the hottest part of the day.")
        steps.append(f"Document the field condition with photos and keep a brief note until the reviewer arrives {reviewer_eta}.")
        return steps[:4]

    steps.append(f"I would isolate the affected plants immediately and follow this first step: {immediate_action}")
    steps.append(f"Please use {water_guidance.get('method', 'drip irrigation only')} and keep the canopy completely dry to reduce disease spread.")
    steps.append(f"For hygiene, {prevention[0] if prevention else 'sanitize your tools and avoid working on wet plants.'}")
    steps.append("I suggest restricting movement through the affected rows and cleaning gloves, knives, and equipment before touching healthy plants.")
    steps.append("Do not wait for the reviewer to start protective action; apply the recommended treatment window as soon as it is safe to do so.")
    steps.append(f"I also recommend logging the current severity at about {confidence:.1f}% and noting the block condition until the reviewer arrives {reviewer_eta}.")
    return steps[:6]


def estimate_yield_forecast(disease_key: str, confidence: float, expected_yield_tons_per_hectare: float = 45.0) -> dict:
    """
    Estimates harvest yield percentage and expected output based on the detected disease and current confidence.
    """
    normalized_key = normalize_class_key(disease_key)
    info = get_disease_info(normalized_key)
    status = info.get("status", "Infected")
    severity = str(info.get("severity", "Moderate")).lower()

    disease_penalty = {
        "tomato_healthy": 0,
        "tomato_bacterial_spot": 42,
        "tomato_early_blight": 30,
        "tomato_late_blight": 68,
        "tomato_leaf_mold": 26,
        "tomato_septoria_leaf_spot": 33,
        "tomato_spider_mites": 20,
        "tomato_target_spot": 24,
        "tomato_mosaic_virus": 55,
        "tomato_yellow_leaf_curl_virus": 60,
    }.get(normalized_key, 25)

    if status == "Healthy":
        yield_percent = max(90.0, min(100.0, 92.0 + (confidence - 50.0) * 0.18))
    else:
        uncertainty_penalty = max(0.0, (100.0 - confidence) * 0.18)
        severity_bonus = 0.0
        if "critical" in severity:
            severity_bonus = 12.0
        elif "high" in severity:
            severity_bonus = 8.0
        elif "moderate" in severity:
            severity_bonus = 4.0
        yield_percent = max(8.0, 100.0 - disease_penalty - uncertainty_penalty - severity_bonus)

    yield_percent = max(8.0, min(100.0, round(yield_percent, 1)))
    estimated_harvest = round(expected_yield_tons_per_hectare * (yield_percent / 100.0), 2)

    return {
        "yield_percent": yield_percent,
        "estimated_harvest_tons_per_hectare": estimated_harvest,
        "expected_yield_tons_per_hectare": expected_yield_tons_per_hectare,
        "yield_loss_percent": round(100.0 - yield_percent, 1),
        "disease_name": info.get("name", "Tomato Crop"),
        "summary": f"Projected harvest is {yield_percent:.1f}% of the normal yield for this crop condition."
    }


def calculate_smart_water_plan(
    disease_key: str,
    growth_stage: str,
    soil_type: str,
    soil_moisture: str,
    weather: str,
    temperature_c: float = 28.0
) -> dict:
    """
    Intelligent agronomical calculation engine for water requirements:
    Evaluates disease susceptibility, plant growth stage, soil water retention,
    current soil moisture status, and ambient weather to determine:
    1. Exact verdict: YES, NO, or REDUCED/DELAYED
    2. Recommended volume (liters/plant)
    3. Optimal watering time
    4. Essential disease-specific watering rules & warnings
    """
    info = get_disease_info(disease_key)
    wg = info.get("water_guidance", {})
    category = info.get("category", "General")

    # Base water volume by growth stage (Liters per plant per day)
    stage_base_volume = {
        "Seedling / Young Plant (Weeks 1-3)": 0.4,
        "Vegetative Growth (Weeks 4-6)": 1.0,
        "Flowering Stage (Weeks 7-9)": 1.6,
        "Fruit Development (Weeks 10-14)": 2.2,
        "Ripening & Harvest (Weeks 15+)": 1.4
    }
    base_vol = stage_base_volume.get(growth_stage, 1.5)

    # Soil retention multiplier
    soil_multipliers = {
        "Sandy Soil (Drains fast, needs more frequent water)": 1.25,
        "Loamy Soil (Optimal moisture holding capacity)": 1.0,
        "Clay Soil (Retains moisture long, risk of waterlogging)": 0.8,
        "Peat / Potting Mix (High water holding)": 0.9
    }
    soil_mult = soil_multipliers.get(soil_type, 1.0)

    # Weather multiplier
    weather_multipliers = {
        "Sunny & Hot (>30°C / 86°F)": 1.35,
        "Moderate & Sunny (22-29°C)": 1.0,
        "Overcast / Cloudy (<22°C)": 0.75,
        "Humid & Sticky (>80% Humidity)": 0.85,
        "Rainy / Wet Day": 0.0
    }
    weather_mult = weather_multipliers.get(weather, 1.0)

    # Adjust for high temperature
    if temperature_c > 32:
        weather_mult *= 1.15
    elif temperature_c < 18:
        weather_mult *= 0.85

    # Compute raw recommended volume
    computed_vol = round(base_vol * soil_mult * weather_mult, 2)

    # Decision logic based on current soil moisture and disease risk
    needs_water = True
    decision = "WATER NOW"
    decision_color = "#10b981"  # green
    urgency = "Standard Watering Window"
    reasoning = []

    if weather == "Rainy / Wet Day":
        needs_water = False
        decision = "NO - RAIN PROVIDES MOISTURE"
        decision_color = "#3b82f6"  # blue
        computed_vol = 0.0
        reasoning.append("Natural precipitation is already hydrating soil. Additional irrigation risks root rot.")
    elif soil_moisture in ["Waterlogged / Saturated", "Very Wet"]:
        needs_water = False
        decision = "NO - SOIL IS ALREADY SATURATED"
        decision_color = "#ef4444"  # red
        computed_vol = 0.0
        reasoning.append("Soil is already saturated. Irrigating now will suffocate roots and promote fungal pythium/rhizoctonia rot.")
    elif soil_moisture == "Adequately Moist (Damp to touch)":
        if "Late Blight" in info["name"] or "Bacterial" in info["name"] or "Early Blight" in info["name"]:
            needs_water = False
            decision = "NO - WITHHOLD WATER (DISEASE RISK)"
            decision_color = "#f59e0b"  # amber
            computed_vol = 0.0
            reasoning.append(f"Soil is still damp. For {info['name']}, letting the topsoil dry restricts pathogen spore movement.")
        else:
            needs_water = False
            decision = "DELAY - SOIL MOISTURE IS SUFFICIENT"
            decision_color = "#3b82f6"
            computed_vol = 0.0
            reasoning.append("Moisture levels are optimal. Re-check topsoil tomorrow morning.")
    elif soil_moisture in ["Bone Dry", "Top 2 Inches Dry"]:
        # Needs water! Check disease constraints
        if "Late Blight" in info["name"]:
            decision = "REDUCED CAUTIONARY DRIP ONLY"
            decision_color = "#ef4444"
            computed_vol = round(max(0.4, computed_vol * 0.6), 2)
            reasoning.append("Soil is dry, but Late Blight poses critical risk. Apply only minimal drip directly to root core; keep canopy 100% dry.")
        elif "Bacterial" in info["name"] or "Early Blight" in info["name"] or "Septoria" in info["name"]:
            decision = "YES - BASE DRIP ONLY (KEEP LEAVES DRY)"
            decision_color = "#f97316"
            computed_vol = round(max(0.5, computed_vol * 0.85), 2)
            reasoning.append("Topsoil is dry. Apply water strictly at ground level beneath mulch. Spattering water will infect higher leaves!")
        elif "Spider Mites" in info["name"]:
            decision = "YES - THOROUGH WATERING + MORNING CANOPY RINSE"
            decision_color = "#10b981"
            computed_vol = round(computed_vol * 1.15, 2)
            reasoning.append("Spider mites thrive on thirsty, drought-stressed plants! Provide thorough base hydration and spray leaf undersides.")
        else:
            decision = "YES - IRRIGATE NOW"
            decision_color = "#10b981"
            reasoning.append("Soil is dry and ready for standard morning irrigation. Water at base to preserve foliage health.")

    return {
        "needs_water": needs_water,
        "decision": decision,
        "decision_color": decision_color,
        "recommended_volume_liters": computed_vol,
        "irrigation_method": wg.get("method", "Base Drip Irrigation"),
        "best_timing": wg.get("best_timing", "Early Morning (6:00 AM - 8:00 AM)"),
        "leaf_wetness_risk": wg.get("leaf_wetness_risk", "Moderate"),
        "rules": wg.get("rules", []),
        "reasoning": reasoning,
        "disease_name": info["name"],
        "category": category
    }
