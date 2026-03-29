#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate SEO landing pages + sitemap.xml for DM Electricals static site.

Targets Nairobi/Kenya search patterns (electrician, fundi, rewiring, CCTV,
electric fence, solar, emergency, neighbourhood names) and AI/overview-friendly
FAQ + entity markup. Run: py -3 scripts/generate_seo_pages.py
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://dmelectricals.com"
TODAY = date.today().isoformat()

ServiceTuple = tuple[str, str, str, str, list[str]]
AreaTuple = tuple[str, str, str, str, list[str]]
ProductTuple = tuple[str, str, str, str, list[str]]

# (slug, title, h1, meta description, body paragraphs)
SERVICES: list[ServiceTuple] = [
    (
        "electrical-industrial-installation-nairobi",
        "Electrical & Industrial Installation Nairobi | DM Electricals",
        "Electrical & industrial installation in Nairobi",
        "Full electrical and industrial installations for homes, offices, and factories across Nairobi. Licensed team, Kenya Power standards, Mwihoko Road, Kasarani. Get a quote.",
        [
            "DM Electricals delivers complete electrical and industrial installations for residential estates, commercial buildings, and manufacturing facilities throughout Nairobi County and surrounding areas. Every project is planned with load calculations, quality materials, and safe cable routing.",
            "We work across Kasarani, Westlands, Ruaraka, Thika Road, Industrial Area, Roysambu, Embakasi, and the wider Nairobi region. Whether you need a new consumer unit, three-phase distribution, or full fit-out for a factory, our team follows ERC-aligned practices and clear documentation.",
            "Request a free site visit from our Mwihoko Road base: call 0799 762 232 or 0762 748 694, or use the contact form on our main website.",
        ],
    ),
    (
        "electrical-fittings-nairobi",
        "Electrical Fittings & Accessories Nairobi | DM Electricals",
        "Electrical fittings, switches & sockets in Nairobi",
        "Supply and installation of switches, sockets, consumer units, and conduits across Nairobi. DM Electricals, Kasarani. Fair pricing, certified work.",
        [
            "We supply and install quality electrical fittings including switches, sockets, distribution boards, conduits, and accessories for renovations and new builds in Nairobi.",
            "We serve homeowners, landlords, and businesses in Kasarani, Westlands, Kilimani, Karen, Ruaraka, and other Nairobi neighbourhoods. Product selection is matched to your budget and Kenya Power requirements.",
            "Contact DM Electricals on Mwihoko Road for fittings and accessories — links to our full product range and enquiry form are on the homepage.",
        ],
    ),
    (
        "appliances-installation-nairobi",
        "Electrical Appliance Installation Nairobi | DM Electricals",
        "Safe installation of cookers, geysers & AC in Nairobi",
        "Certified installation of cookers, water heaters, air conditioners, and industrial machinery. Nairobi-wide service from DM Electricals, Kasarani.",
        [
            "Incorrect appliance installation is a leading cause of fire and shock risk. DM Electricals connects cookers, ovens, water heaters, air conditioners, washing machines, and industrial equipment safely and to manufacturer specification.",
            "We cover residential and commercial clients across Nairobi, including estates along Thika Road, Mombasa Road, Ngong Road, and local areas such as Kasarani and Roysambu.",
            "Book installation or discuss your requirements via the contact section on our main site.",
        ],
    ),
    (
        "electrical-cables-nairobi",
        "Electrical Cables & Wiring Nairobi | DM Electricals",
        "Power cables, armoured cable & data in Nairobi",
        "Supply and installation of power cables, armoured cables, and data cabling for Nairobi homes and businesses. DM Electricals — Mwihoko Road, Kasarani.",
        [
            "We supply and install PVC armoured cable, twin and earth, flexible copper, and conduit systems for residential, commercial, and industrial projects in Nairobi.",
            "Our team supports rewires, extensions, and new construction across Nairobi County and nearby towns including Kiambu and Ruiru where travel is agreed.",
            "Enquire about cable sizing, routing, and protection — full catalogue and WhatsApp on our main website.",
        ],
    ),
    (
        "electric-fence-nairobi",
        "Electric Fence Installation Nairobi | DM Electricals",
        "Electric fence & energisers in Nairobi",
        "Perimeter electric fencing for homes, estates, and commercial plots in Nairobi. Energisers, earthing, alarms, and compliance. DM Electricals Kasarani.",
        [
            "Electric fence systems deter intrusion and integrate with sirens and alarms. DM Electricals designs, supplies, and installs energisers, high-tensile wire, earthing, and warning signage for compounds in Nairobi.",
            "We have completed projects in Roysambu, Kasarani, Ruaraka, Thika Road corridors, Karen, and other residential and commercial locations. Many clients search for an electric fence installer Nairobi — we provide full perimeter packages.",
            "Get a site assessment and quote — contact details and project gallery on our homepage.",
        ],
    ),
    (
        "fire-alarm-systems-nairobi",
        "Fire Detection & Alarm Systems Nairobi | DM Electricals",
        "Fire alarms, smoke detectors & panels in Nairobi",
        "Fire detection, smoke alarms, and addressable panels for commercial and industrial buildings in Nairobi. DM Electricals — certified workmanship.",
        [
            "We install fire detection, smoke and heat detectors, manual call points, and fire alarm panels for multi-level buildings, warehouses, schools, and offices in Nairobi.",
            "Projects are coordinated with your building layout and safety requirements. We serve Westlands, Industrial Area, Thika Road business parks, and wider Nairobi.",
            "Discuss your building type and certification needs — visit our main site for contact options and recent projects.",
        ],
    ),
    (
        "cctv-security-nairobi",
        "CCTV & Security Cameras Nairobi | DM Electricals",
        "CCTV installation, IP cameras & NVR in Nairobi",
        "CCTV and IP camera systems for homes, shops, and estates in Nairobi. Remote viewing, NVR, night vision. DM Electricals Kasarani.",
        [
            "We supply and install HD and IP CCTV systems with NVR/DVR recording, remote mobile access, and motion detection for homes, offices, retail, and estates across Nairobi.",
            "Coverage includes Kasarani, Ruaraka, Westlands, Thika Road, Eastleigh, South B, Embakasi, and apartment complexes across the city.",
            "See our portfolio and request a quote on the main DM Electricals website.",
        ],
    ),
    (
        "wiring-rewiring-nairobi",
        "House Rewiring & Wiring Nairobi | DM Electricals",
        "Full rewiring & new wiring in Nairobi",
        "Complete rewiring, fault finding, and new construction electrical layouts. Kenya Power compliant. DM Electricals — Nairobi electricians.",
        [
            "Old wiring and overloaded circuits need professional rewiring. DM Electricals performs full property rewires, partial upgrades, consumer unit replacements, and fault finding for residential and commercial buildings in Nairobi.",
            "We work in older homes, new builds, and renovations across Nairobi neighbourhoods and nearby Kiambu County when requested.",
            "Call for inspection or quote — details on our homepage.",
        ],
    ),
    (
        "emergency-electrician-nairobi",
        "24/7 Emergency Electrician Nairobi | DM Electricals",
        "Emergency electrician — 24/7 in Nairobi",
        "Rapid response for tripped breakers, outages, short circuits, and electrical hazards in Nairobi. DM Electricals — emergency line 0799 762 232.",
        [
            "Electrical emergencies can happen day or night. DM Electricals offers round-the-clock response for power failures, tripping breakers, burning smells, sparks, and dangerous faults across Nairobi. Customers often search emergency electrician near me Nairobi — we dispatch from our Kasarani base.",
            "Our team aims to attend emergency calls quickly — often within an hour depending on location and traffic — from Kasarani and throughout Nairobi.",
            "Save our numbers: 0799 762 232 and 0762 748 694. Full contact and WhatsApp on our main website.",
        ],
    ),
    # —— Additional service pages (search-intent / GEO / AIO expansion) ——
    (
        "solar-electrical-installation-nairobi",
        "Solar Electrical Installation Nairobi | Panels, Inverters & Integration | DM Electricals",
        "Solar panels, inverters & electrical integration in Nairobi",
        "Solar panel and hybrid inverter installation with correct AC/DC integration, earthing, and protection for Nairobi homes and businesses. DM Electricals Mwihoko Road, Kasarani.",
        [
            "Solar backup and grid-tie systems need safe electrical integration — string wiring, inverter locations, surge protection, and earthing. DM Electricals installs and commissions solar electrical works alongside quality solar components.",
            "We support residential estates, schools, and commercial rooftops across Nairobi and greater Kiambu where schedules allow. Popular searches include solar installation Nairobi and inverter backup electrician.",
            "Combine solar pages on our main site with this guide, then call 0799 762 232 or use the homepage WhatsApp for a site assessment.",
        ],
    ),
    (
        "generator-backup-electrical-nairobi",
        "Generator & Backup Power Electrical Nairobi | Changeover & ATS | DM Electricals",
        "Generator hookup, changeover switches & backup power in Nairobi",
        "Generator electrical hookups, manual changeover, and ATS coordination for Nairobi properties. Safe earthing and Kenya Power–aware designs. DM Electricals.",
        [
            "Backup generators require correct changeover or automatic transfer, neutral-earth bonding rules, and cable sizing. DM Electricals installs generator feeds, interlocks, and distribution so mains and generator do not back-feed dangerously.",
            "We serve homes, hotels, and light industrial clients across Nairobi County. Works hand-in-hand with our changeover and UPS product supply on the main website.",
            "Request a load survey and quote via the main DM Electricals contact section.",
        ],
    ),
    (
        "electrical-fault-repairs-nairobi",
        "Electrical Fault Finding & Repairs Nairobi | Sockets, Breakers | DM Electricals",
        "Socket repair, tripping breakers & electrical fault finding in Nairobi",
        "Affordable circuit repairs, socket replacements, and fault finding in Nairobi. Fix tripping breakers, partial power loss, and unsafe outlets. DM Electricals.",
        [
            "Many Nairobi searches are for a verified fundi for wiring Nairobi or socket repair — professional fault finding avoids repeated tripping and fire risk. DM Electricals traces earth faults, overloads, and damaged accessories.",
            "We repair and replace sockets, lighting circuits, cooker outlets, and distribution faults for flats, houses, and shops in Kasarani, Westlands, Eastleigh, Embakasi, and county-wide.",
            "Book a visit: 0799 762 232 / 0762 748 694 or WhatsApp from the homepage.",
        ],
    ),
    (
        "lighting-installation-nairobi",
        "Lighting Installation Nairobi | LED, Outdoor & Security Lights | DM Electricals",
        "Indoor & outdoor lighting installation in Nairobi",
        "LED downlights, panel lights, outdoor floods, and pathway lighting installed across Nairobi. DM Electricals supply and fit.",
        [
            "From recessed LEDs to security floodlights and estate pathway lighting, we install energy-efficient lighting with correct switching and zones. Matches our LED and floodlight product pages.",
            "We complete lighting upgrades for homes in Kilimani, Karen, South B, Parklands, and commercial fit-outs in Westlands and Upper Hill.",
            "See the lighting products on our homepage and contact us for design and installation.",
        ],
    ),
    (
        "smart-home-electrical-nairobi",
        "Smart Home Electrician Nairobi | Switches, Curtains & Locks | DM Electricals",
        "Smart home electrical installation in Nairobi",
        "Wi‑Fi and Zigbee smart switches, motorized curtains, and smart locks — installed by licensed electricians in Nairobi. DM Electricals.",
        [
            "Smart lighting and access control need neutral where required, proper loads, and network planning. DM Electricals installs smart switches, curtain motors, and digital locks for modern homes and offices.",
            "Ideal for apartments in Kilimani, Lavington, Kileleshwa, and new builds along Ngong Road. Cross-links to our smart product landing pages.",
            "Enquire via the main website catalogue or call our office lines.",
        ],
    ),
]

PRODUCTS: list[ProductTuple] = [
    (
        "pvc-armoured-cable-nairobi",
        "PVC Armoured Cable Supply Nairobi | DM Electricals",
        "PVC armoured cable (2.5mm–25mm²) for Nairobi",
        "Heavy-duty PVC armoured cables for underground and surface installations in Nairobi. Enquire via DM Electricals — Mwihoko Road, Kasarani.",
        ["Armoured PVC cables for mains and submains, suitable for residential and commercial installations in Nairobi and surrounds. We supply and install with correct termination and protection.", "Contact us for sizes and pricing — see our product catalogue on the main site."],
    ),
    (
        "flat-twin-earth-cable-nairobi",
        "Twin & Earth Cable Nairobi | DM Electricals",
        "Flat twin and earth cable (T&E) Nairobi",
        "Standard twin and earth cable for internal wiring in Nairobi homes and offices. DM Electricals — supply and installation.",
        ["T&E cable for ring circuits, lighting, and sockets. We supply and install across Nairobi for compliance and safety.", "WhatsApp product enquiries from our main website."],
    ),
    (
        "flexible-copper-wire-nairobi",
        "Flexible Copper Wire & Cable Nairobi | DM Electricals",
        "Flexible single and multi-core copper cable Nairobi",
        "Flexible copper cables for appliances and industrial connections. DM Electricals, Nairobi.",
        ["Multi-core and flexible copper for panels, machinery, and appliance tails. Available in Nairobi through DM Electricals.", "Full range listed on the homepage."],
    ),
    (
        "pvc-conduit-pipes-nairobi",
        "PVC Conduit & Trunking Nairobi | DM Electricals",
        "PVC conduit pipes and accessories Nairobi",
        "Heavy and light gauge PVC conduit, bends, and junction boxes for Nairobi wiring projects. DM Electricals.",
        ["Conduit systems for surface and concealed wiring. We supply and install across Nairobi for residential and commercial projects.", "Enquire on the main site."],
    ),
    (
        "mcb-consumer-units-nairobi",
        "Consumer Units & Distribution Boards Nairobi | DM Electricals",
        "MCB consumer units and distribution boards Nairobi",
        "Single and three-phase consumer units from 4-way to 24-way. DM Electricals supply Nairobi.",
        ["Consumer units for houses, flats, and shops. Correct sizing and protection for Nairobi installations.", "See main site for specifications."],
    ),
    (
        "switches-sockets-nairobi",
        "Switches & Sockets Nairobi | DM Electricals",
        "Electrical switches, sockets & USB outlets Nairobi",
        "Switches, sockets, weatherproof outlets, and USB options for Nairobi homes and businesses. DM Electricals.",
        ["Modern fittings and accessories for upgrades and new builds. We install across Nairobi and neighbouring areas.", "Contact via homepage."],
    ),
    (
        "smart-switches-nairobi",
        "Smart Switches Nairobi | DM Electricals",
        "Wi‑Fi and Zigbee smart switches Nairobi",
        "Smart touch and dimmer switches with app and voice control. Supply and installation in Nairobi. DM Electricals.",
        ["Wi‑Fi / Zigbee switches for lighting scenes and automation. We supply and install across Nairobi.", "Enquire on the main site."],
    ),
    (
        "smart-curtains-nairobi",
        "Smart Curtains & Motorized Tracks Nairobi | DM Electricals",
        "Motorized curtains and blinds Nairobi",
        "Motorized curtain tracks and smart blinds — remote and timer control. DM Electricals Nairobi.",
        ["Residential and commercial motorized window treatments. Installation across Nairobi.", "See homepage for contact."],
    ),
    (
        "smart-locks-nairobi",
        "Smart Door Locks Nairobi | DM Electricals",
        "Fingerprint and app smart locks Nairobi",
        "Digital smart locks — fingerprint, PIN, card, and app unlock. DM Electricals supply and install in Nairobi.",
        ["Smart locks for homes and offices with audit trails. Nairobi-wide service.", "WhatsApp from main site."],
    ),
    (
        "mcbs-rcds-nairobi",
        "MCBs & RCDs Nairobi | DM Electricals",
        "MCB and RCD protection devices Nairobi",
        "Miniature circuit breakers and RCDs for overload and earth fault protection. DM Electricals Nairobi.",
        ["Correct protection for split circuits and compliance. We supply and install across Nairobi.", "Product catalogue on main page."],
    ),
    (
        "cable-trays-trunking-nairobi",
        "Cable Trays & Trunking Nairobi | DM Electricals",
        "Steel cable trays, trunking & ducting Nairobi",
        "Cable management systems for commercial and industrial sites in Nairobi. DM Electricals.",
        ["Trays and trunking for neat cable runs in offices, factories, and warehouses. Nairobi-wide service.", "Request quote on main site."],
    ),
    (
        "cctv-ip-systems-nairobi",
        "CCTV IP Camera Kits Nairobi | DM Electricals",
        "IP CCTV systems and NVR Nairobi",
        "IP CCTV cameras with NVR suites for Nairobi homes and businesses. Night vision and motion detection. DM Electricals.",
        ["Indoor and outdoor IP cameras with remote viewing. Installed across Nairobi and surrounding estates.", "See portfolio on main site."],
    ),
    (
        "electric-fence-energiser-nairobi",
        "Electric Fence Energiser Nairobi | DM Electricals",
        "Mains and solar energisers for electric fence Nairobi",
        "Electric fence energisers for residential and commercial perimeters in Nairobi. DM Electricals — supply and installation.",
        ["Mains and solar energisers with alarm integration. We install in Nairobi and surrounding areas.", "Main website for contact."],
    ),
    (
        "burglar-alarm-systems-nairobi",
        "Burglar Alarm Systems Nairobi | DM Electricals",
        "Intruder alarm kits and PIR sensors Nairobi",
        "Full burglar alarm systems with PIR, contacts, siren, and panel. DM Electricals Nairobi.",
        ["Residential and commercial alarm packages. Installation across Nairobi with user training.", "Enquire via homepage."],
    ),
    (
        "smoke-detectors-fire-panels-nairobi",
        "Smoke Detectors & Fire Panels Nairobi | DM Electricals",
        "Smoke detectors and fire alarm panels Nairobi",
        "Photoelectric smoke detectors and addressable fire panels for Nairobi buildings. DM Electricals.",
        ["Detection and panels for compliance and safety. Commercial and industrial projects in Nairobi.", "Contact main site."],
    ),
    (
        "electric-water-heaters-nairobi",
        "Electric Water Heaters & Geysers Nairobi | DM Electricals",
        "Electric geyser and water heater installation Nairobi",
        "Instant and storage electric water heaters for homes and business in Nairobi. DM Electricals installation.",
        ["Correct cable sizing and isolation for geysers. Nairobi-wide installation service.", "Call or WhatsApp on main site."],
    ),
    (
        "cooker-connection-units-nairobi",
        "Cooker Connection Units Nairobi | DM Electricals",
        "45A cooker outlets and heavy cable Nairobi",
        "Cooker connection units and heavy-duty cable for electric cookers and hobs. DM Electricals Nairobi.",
        ["Safe installation for kitchen appliances. We serve homes across Nairobi.", "Main website contact."],
    ),
    (
        "led-lighting-nairobi",
        "LED Downlights & Panel Lights Nairobi | DM Electricals",
        "LED panel lights and downlights Nairobi",
        "Recessed LED panels and downlights for ceilings in Nairobi homes and offices. DM Electricals.",
        ["Energy-efficient LED lighting for residential and commercial projects. Installed across Nairobi.", "See products on homepage."],
    ),
    (
        "security-floodlights-nairobi",
        "LED Security Floodlights Nairobi | DM Electricals",
        "Outdoor motion floodlights Nairobi",
        "LED floodlights with PIR for perimeter security in Nairobi. DM Electricals supply and install.",
        ["Outdoor security lighting for compounds and driveways. Available throughout Nairobi.", "Contact main site."],
    ),
    (
        "street-pathway-lights-nairobi",
        "Street & Pathway LED Lights Nairobi | DM Electricals",
        "Street lights and pathway bollards Nairobi",
        "Street and pathway lighting for estates and parking in Nairobi. DM Electricals.",
        ["LED street and area lighting for estates and commercial plots. Nairobi-wide service.", "Enquire on homepage."],
    ),
    (
        "ups-systems-nairobi",
        "UPS Systems Nairobi | DM Electricals",
        "UPS backup power Nairobi",
        "Online and offline UPS for computers, servers, and critical loads in Nairobi. DM Electricals.",
        ["UPS sizing and installation for offices and homes. Nairobi and surrounds.", "Product catalogue on main page."],
    ),
    (
        "voltage-stabilisers-nairobi",
        "Voltage Stabilisers & AVR Nairobi | DM Electricals",
        "Automatic voltage regulators (AVR) Nairobi",
        "AVRs for fluctuating Kenya Power supply — protect appliances in Nairobi. DM Electricals.",
        ["Voltage stabilisers for sensitive equipment. Supply and install across Nairobi.", "Main website."],
    ),
    (
        "changeover-ats-switches-nairobi",
        "Changeover & ATS Switches Nairobi | DM Electricals",
        "Generator changeover and ATS Nairobi",
        "Manual and automatic transfer switches between mains and generator power. DM Electricals Nairobi.",
        ["Changeover and ATS for seamless backup power. Installed in Nairobi homes and businesses.", "Contact main site."],
    ),
    (
        "solar-panels-inverters-nairobi",
        "Solar Panels & Inverters Nairobi | DM Electricals",
        "Solar panels, hybrid inverters & batteries Nairobi",
        "Solar panels, hybrid inverters, charge controllers, and batteries for Nairobi homes and businesses. DM Electricals.",
        ["Solar components and installation support. Greater Nairobi and surrounding areas.", "WhatsApp on homepage."],
    ),
]

AREAS: list[AreaTuple] = [
    (
        "electrician-kasarani-nairobi",
        "Electrician Kasarani | DM Electricals Mwihoko Road",
        "Electrician in Kasarani — Mwihoko Road based",
        "Licensed electricians in Kasarani, Nairobi. DM Electricals is based on Mwihoko Road — installations, CCTV, electric fence, emergencies. Call 0799 762 232.",
        [
            "Kasarani residents and businesses rely on DM Electricals for fast, professional electrical work. We are based on Mwihoko Road — close to Mwiki, Roysambu, and the wider Kasarani constituency.",
            "Services include rewiring, new builds, CCTV, electric fence, fire alarms, three-phase installations, and 24/7 emergency response. Fair pricing and transparent quotes.",
            "Visit our homepage for the full service list, portfolio, and contact form.",
        ],
    ),
    (
        "electrician-westlands-nairobi",
        "Electrician Westlands Nairobi | DM Electricals",
        "Electrical & alarm systems in Westlands Nairobi",
        "Commercial and residential electrical fit-outs in Westlands — office lighting, fire alarms, UPS, data. DM Electricals from Nairobi.",
        [
            "Westlands commercial complexes, restaurants, and offices need reliable electrical and fire alarm systems. DM Electricals has completed installations across the Nairobi CBD and business districts.",
            "We coordinate site surveys, structured cabling, and compliance documentation for your project.",
            "Contact us via the main website for Westlands enquiries.",
        ],
    ),
    (
        "electrician-ruaraka-nairobi",
        "Electrician Ruaraka Nairobi | DM Electricals",
        "Electrical rewiring and repairs in Ruaraka",
        "Rewiring, CCTV, and installations for homes and businesses in Ruaraka, Nairobi. DM Electricals.",
        [
            "Ruaraka is within our regular service area across northern Nairobi. We handle full rewires, security lighting, and consumer unit upgrades.",
            "See our portfolio for a Ruaraka rewiring project example — more details on the homepage.",
        ],
    ),
    (
        "electrician-thika-road-nairobi",
        "Electrician Thika Road Nairobi | DM Electricals",
        "Electrical work along Thika Road corridor",
        "Offices, apartments, and retail along Thika Road — electrical installation and CCTV. DM Electricals Nairobi.",
        [
            "From Roysambu to Muthaiga, Thika Road is one of Nairobi's busiest corridors. We install commercial electrical systems, UPS, structured cabling, and smart lighting for multi-floor buildings.",
            "Contact DM Electricals for projects along Thika Road and surrounding estates.",
        ],
    ),
    (
        "electrician-industrial-area-nairobi",
        "Industrial Electrician Nairobi Industrial Area | DM Electricals",
        "3-phase industrial electrical in Nairobi Industrial Area",
        "Factory power, motor control, motor control panels, and earthing in Industrial Area, Nairobi. DM Electricals.",
        [
            "Industrial Area factories and warehouses need three-phase distribution, motor controls, and earthing that meets safety standards. DM Electricals delivers industrial electrical installations.",
            "We serve manufacturing and logistics clients across Nairobi.",
        ],
    ),
    (
        "electrician-roysambu-nairobi",
        "Electrician Roysambu Nairobi | DM Electricals",
        "Electric fence & residential electrical in Roysambu",
        "Residential electrical work, electric fence, and CCTV in Roysambu, Nairobi. DM Electricals Kasarani.",
        [
            "Roysambu estates and compounds benefit from our local expertise in perimeter fencing and domestic electrical. We have completed electric fence projects in the area.",
            "Contact us via the main website for Roysambu service calls.",
        ],
    ),
    (
        "electrician-kilimani-nairobi",
        "Electrician Kilimani Nairobi | DM Electricals",
        "Electrical renovations and upgrades in Kilimani",
        "Appliances, fittings, and lighting upgrades in Kilimani apartments and homes. DM Electricals Nairobi.",
        [
            "Kilimani and nearby neighbourhoods require discreet, professional electrical work for apartments and townhouses. DM Electricals handles upgrades, appliance installation, and fault finding.",
        ],
    ),
    (
        "electrician-karen-nairobi",
        "Electrician Karen Nairobi | DM Electricals",
        "Electrical for homes and compounds in Karen",
        "Large homes and estates in Karen — full electrical, CCTV, solar, and gate systems. DM Electricals Nairobi.",
        [
            "Karen properties often need comprehensive electrical design, CCTV, backup power, and outdoor lighting. We travel from our Kasarani base for agreed projects across Karen and Langata.",
        ],
    ),
    (
        "electrician-mombasa-road-nairobi",
        "Electrician Mombasa Road Nairobi | DM Electricals",
        "Commercial electrical along Mombasa Road",
        "Warehouses, factories, and logistics along Mombasa Road — electrical and industrial installation. DM Electricals.",
        [
            "Mombasa Road industrial zones and retail parks require industrial-fit electrical work. DM Electricals supports commercial and industrial clients along the corridor.",
        ],
    ),
    (
        "electrician-eastleigh-nairobi",
        "Electrician Eastleigh Nairobi | DM Electricals",
        "Electrical for shops and buildings in Eastleigh",
        "Retail and commercial electrical fit-outs in Eastleigh, Nairobi. DM Electricals.",
        [
            "Dense retail and commercial areas need reliable power and lighting. DM Electricals serves shops and buildings across Eastleigh with professional installation and repair.",
        ],
    ),
    (
        "electrical-contractor-kiambu-ruiru",
        "Electrical Contractor Kiambu & Ruiru | DM Electricals",
        "Electrical services extending to Kiambu & Ruiru",
        "Electrical installations and call-outs in Kiambu County — Ruiru, Ruaka, Thika, and surrounding areas. DM Electricals Nairobi.",
        [
            "Many clients outside Nairobi County ask for our services. We travel to Kiambu County, including Ruiru, Ruaka, and parts of Thika, depending on project scope and scheduling.",
            "Contact us for larger projects or emergencies — we coordinate from our Nairobi base.",
        ],
    ),
    (
        "electrical-services-nairobi-county",
        "Electrical Services Nairobi County | DM Electricals",
        "Electrical contractor covering Nairobi County",
        "Licensed electrical contractor covering all of Nairobi County — homes, offices, industrial. DM Electricals — Mwihoko Road, Kasarani.",
        [
            "Nairobi County covers the CBD, Westlands, Kasarani, Embakasi, Kibra, Langata, Roysambu, and many sub-locations. DM Electricals provides electrical installation, maintenance, and emergency repairs across the county.",
            "Whether you are in Kileleshwa, Southlands, Upper Hill, or along the northern bypass, we aim to respond to enquiries and emergencies professionally.",
            "Our full service list, products, and testimonials are on the homepage.",
        ],
    ),
    # High-intent neighbourhood / corridor pages
    (
        "electrician-embakasi-nairobi",
        "Electrician Embakasi Nairobi | DM Electricals",
        "Electrician in Embakasi — repairs, CCTV & wiring",
        "Electrical installations, CCTV, rewiring, and emergency electrician in Embakasi, Nairobi. DM Electricals — 0799 762 232.",
        [
            "Embakasi and surrounding estates have high demand for reliable fundis and licensed electricians for sockets, lighting, water heaters, and security systems.",
            "DM Electricals provides transparent quotes, ERC-aligned work, and support for both residential blocks and small businesses in Embakasi.",
        ],
    ),
    (
        "electrician-south-b-nairobi",
        "Electrician South B Nairobi | DM Electricals",
        "Electrician in South B — homes & apartments",
        "Rewiring, appliance installation, CCTV, and fault repairs in South B, Nairobi. Call DM Electricals 0799 762 232.",
        [
            "South B and South C corridors are busy residential zones — we handle consumer unit upgrades, new lighting, and emergency call-outs.",
            "Book a visit via our homepage or WhatsApp for same-week scheduling where capacity allows.",
        ],
    ),
    (
        "electrician-ngong-road-nairobi",
        "Electrician Ngong Road Nairobi | DM Electricals",
        "Electrical along Ngong Road & valley",
        "Commercial and residential electrical work along Ngong Road — offices, apartments, restaurants. DM Electricals Nairobi.",
        [
            "Ngong Road hosts retail, hospitality, and residential developments that need compliant lighting, three-phase feeds, and backup integration.",
            "DM Electricals coordinates site surveys and installation timelines with landlords and facilities teams.",
        ],
    ),
    (
        "electrician-upper-hill-nairobi",
        "Electrician Upper Hill Nairobi | DM Electricals",
        "Commercial electrical in Upper Hill",
        "Office towers and institutions in Upper Hill — lighting, UPS, fire alarms, data power. DM Electricals.",
        [
            "Upper Hill is a dense commercial node; we support fit-outs, fire detection, and critical power for professional buildings.",
            "Contact DM Electricals for tender-ready documentation and professional installation teams.",
        ],
    ),
    (
        "electrician-parklands-nairobi",
        "Electrician Parklands Nairobi | DM Electricals",
        "Electrical services in Parklands & Chiromo",
        "Homes, schools, and clinics in Parklands — wiring, lighting upgrades, alarms. DM Electricals Nairobi.",
        [
            "Parklands mixes residential and institutional buildings needing safe upgrades and transparent pricing.",
            "We serve rewires, new circuits, CCTV, and emergency faults across the neighbourhood.",
        ],
    ),
    (
        "electrician-lavington-nairobi",
        "Electrician Lavington Nairobi | DM Electricals",
        "Electrical & smart home in Lavington",
        "Premium homes in Lavington — lighting, smart switches, generators, solar integration. DM Electricals.",
        [
            "Lavington homeowners often request aesthetic lighting, smart home devices, and reliable backup solutions.",
            "DM Electricals delivers neat workmanship and product guidance aligned with our smart-home service pages.",
        ],
    ),
    (
        "electrician-kileleshwa-nairobi",
        "Electrician Kileleshwa Nairobi | DM Electricals",
        "Apartments & townhouses in Kileleshwa",
        "Electrical repairs, appliance installs, and upgrades in Kileleshwa, Nairobi. DM Electricals.",
        [
            "High-density apartments need fast fault finding and careful noise-aware scheduling.",
            "We install cookers, water heaters, lighting, and security systems for Kileleshwa residents.",
        ],
    ),
]

PROVIDER = {
    "@type": ["Electrician", "LocalBusiness"],
    "@id": f"{BASE}/#provider",
    "name": "DM Electricals & Installation",
    "url": f"{BASE}/",
    "telephone": "+254799762232",
    "email": "info@dmelectricals.com",
    "priceRange": "$$",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "Mwihoko Road",
        "addressLocality": "Kasarani",
        "addressRegion": "Nairobi County",
        "addressCountry": "KE",
    },
    "geo": {"@type": "GeoCoordinates", "latitude": -1.228, "longitude": 36.899},
    "areaServed": [{"@type": "City", "name": "Nairobi"}, {"@type": "AdministrativeArea", "name": "Nairobi County"}],
}


def _breadcrumb(path_from_root: str, h1: str) -> list[dict]:
    crumbs = [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
    ]
    if path_from_root.startswith("services/"):
        crumbs.append({"@type": "ListItem", "position": 2, "name": "Services", "item": f"{BASE}/#services"})
        crumbs.append({"@type": "ListItem", "position": 3, "name": h1, "item": f"{BASE}/{path_from_root}"})
    elif path_from_root.startswith("products/"):
        crumbs.append({"@type": "ListItem", "position": 2, "name": "Products", "item": f"{BASE}/#products"})
        crumbs.append({"@type": "ListItem", "position": 3, "name": h1, "item": f"{BASE}/{path_from_root}"})
    elif path_from_root.startswith("areas/"):
        crumbs.append({"@type": "ListItem", "position": 2, "name": "Areas", "item": f"{BASE}/#contact"})
        crumbs.append({"@type": "ListItem", "position": 3, "name": h1, "item": f"{BASE}/{path_from_root}"})
    return crumbs


def _faq_entities(h1: str, kind: str) -> list[dict]:
    base_q: list[tuple[str, str]] = [
        (
            "How do I contact DM Electricals for a quote in Nairobi?",
            "Call 0799 762 232 or 0762 748 694, email info@dmelectricals.com, or use the contact form and WhatsApp links on the main website at dmelectricals.com. We typically respond the same business day.",
        ),
        (
            "Does DM Electricals offer emergency electrical service in Nairobi?",
            "Yes. We provide 24/7 emergency electrician support for tripping breakers, partial power loss, burning smells, and hazardous faults across Nairobi County, dispatching from our Kasarani base.",
        ),
        (
            "Where is DM Electricals based and which areas do you serve?",
            "We are based on Mwihoko Road, Kasarani, Nairobi. We regularly serve Kasarani, Roysambu, Westlands, Ruaraka, Thika Road, Embakasi, South B, Kilimani, Karen, Industrial Area, Mombasa Road, Eastleigh, Ngong Road, Upper Hill, Parklands, Lavington, Kileleshwa, and the wider Nairobi County. Kiambu and Ruiru by arrangement.",
        ),
    ]
    if kind == "service":
        base_q.insert(
            0,
            (
                f"Who installs or repairs {h1.split(' in ')[0]} in Nairobi?",
                "DM Electricals & Installation is a licensed electrical contractor based on Mwihoko Road, Kasarani. We supply, install, and maintain electrical, security, and backup systems across Nairobi with ERC-aligned workmanship.",
            ),
        )
    elif kind == "area":
        base_q.insert(
            0,
            (
                f"Is there a reliable electrician for residential and commercial work near {h1}?",
                "DM Electricals serves this neighbourhood from our Kasarani base with rewiring, installations, CCTV, electric fence, fire alarms, solar integration, and emergency call-outs. Contact us for a site visit or fast fault response.",
            ),
        )
    else:
        base_q.insert(
            0,
            (
                f"Where can I buy or get installed {h1.split(' in ')[0]} in Nairobi?",
                "DM Electricals supplies and installs this product line across Nairobi with correct cabling, protection, and warranty-friendly workmanship. Enquire via the main catalogue or WhatsApp.",
            ),
        )
    return [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in base_q]


def link_hub_html(kind: str, slug: str) -> str:
    """Dense internal linking for crawlers and AI entity discovery."""
    blocks: list[str] = []
    blocks.append('<nav class="hub" aria-label="Related pages on this site">')
    blocks.append("<h2>More from DM Electricals</h2>")

    blocks.append("<h3>Electrical services (Nairobi)</h3><ul>")
    for s, _t, h1s, _m, _p in SERVICES:
        if kind == "service" and s == slug:
            continue
        blocks.append(f'<li><a href="{BASE}/services/{escape(s)}.html">{escape(h1s)}</a></li>')
    blocks.append("</ul>")

    blocks.append("<h3>Service areas &amp; locations</h3><ul>")
    for s, _t, h1s, _m, _p in AREAS:
        if kind == "area" and s == slug:
            continue
        blocks.append(f'<li><a href="{BASE}/areas/{escape(s)}.html">{escape(h1s)}</a></li>')
    blocks.append("</ul>")

    blocks.append("<h3>Popular products</h3><ul>")
    for i, (s, _t, h1s, _m, _p) in enumerate(PRODUCTS):
        if kind == "product" and s == slug:
            continue
        if i >= 12:
            break
        blocks.append(f'<li><a href="{BASE}/products/{escape(s)}.html">{escape(h1s)}</a></li>')
    blocks.append(f'<li><a href="{BASE}/#products"><strong>Full product catalogue on homepage →</strong></a></li>')
    blocks.append("</ul>")
    blocks.append("</nav>")
    return "\n  ".join(blocks)


def page_html(path_from_root: str, title: str, h1: str, meta: str, paras: list[str], *, kind: str, slug: str) -> str:
    canonical = f"{BASE}/{path_from_root}"
    body = "".join(f"<p>{escape(p)}</p>" for p in paras)
    hub = link_hub_html(kind, slug)

    faq_items = _faq_entities(h1, kind)
    faq_node = {"@type": "FAQPage", "mainEntity": faq_items}
    breadcrumb_node = {"@type": "BreadcrumbList", "itemListElement": _breadcrumb(path_from_root, h1)}
    web_page = {
        "@type": "WebPage",
        "name": title,
        "description": meta,
        "url": canonical,
        "inLanguage": "en-KE",
        "isPartOf": {"@type": "WebSite", "name": "DM Electricals & Installation", "url": f"{BASE}/"},
    }

    graph: list[dict] = [web_page, breadcrumb_node, faq_node]

    if kind == "service":
        graph.append(
            {
                "@type": "Service",
                "name": h1,
                "description": meta,
                "url": canonical,
                "provider": {"@id": PROVIDER["@id"]},
                "serviceType": "Electrical contracting",
                "areaServed": {"@type": "City", "name": "Nairobi"},
            }
        )

    graph.append(dict(PROVIDER))

    ld_blob = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)

    og = (
        f'<meta property="og:type" content="website">\n'
        f'<meta property="og:url" content="{escape(canonical)}">\n'
        f'<meta property="og:title" content="{escape(title)}">\n'
        f'<meta property="og:description" content="{escape(meta)}">\n'
        f'<meta property="og:locale" content="en_KE">\n'
        f'<meta name="twitter:card" content="summary">\n'
        f'<meta name="twitter:title" content="{escape(title)}">\n'
        f'<meta name="twitter:description" content="{escape(meta)}">\n'
    )

    geo_meta = ""
    if kind == "area":
        geo_meta = (
            '<meta name="geo.region" content="KE-30">\n'
            '<meta name="geo.placename" content="Nairobi, Kenya">\n'
            '<meta name="ICBM" content="-1.228, 36.899">\n'
        )

    return f"""<!DOCTYPE html>
<html lang="en-KE">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{escape(title)}</title>
<meta name="description" content="{escape(meta)}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="en-KE" href="{canonical}">
<link rel="alternate" hreflang="en" href="{canonical}">
{geo_meta}{og}<link rel="icon" type="image/svg+xml" href="{BASE}/favicon.svg">
<link rel="icon" type="image/x-icon" href="{BASE}/favicon.ico" sizes="48x48 32x32 16x16">
<link rel="shortcut icon" href="{BASE}/favicon.ico">
<link rel="apple-touch-icon" href="{BASE}/favicon.ico">
<style>
body{{font-family:system-ui,-apple-system,'Segoe UI',sans-serif;line-height:1.65;max-width:720px;margin:0 auto;padding:2rem 1.25rem;color:#111827;background:#F8F8F8}}
a{{color:#8B1A2E;font-weight:600}}
h1{{font-size:1.5rem;line-height:1.25;margin-bottom:1rem}}
h2{{font-size:1.15rem;margin:1.75rem 0 0.75rem}}
h3{{font-size:0.95rem;margin:1.25rem 0 0.5rem;color:#374151}}
header{{margin-bottom:1.5rem;padding-bottom:1rem;border-bottom:1px solid #e5e7eb}}
footer{{margin-top:2rem;padding-top:1rem;border-top:1px solid #e5e7eb;font-size:0.875rem;color:#6b7280}}
.hub{{margin-top:2rem;padding:1.25rem;background:#fff;border:1px solid #e5e7eb;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,0.04)}}
.hub ul{{margin:0.35rem 0 0.85rem 1rem;padding:0}}
.hub li{{margin:0.35rem 0}}
</style>
<script type="application/ld+json">{ld_blob}</script>
</head>
<body>
<header>
  <nav aria-label="Breadcrumb"><a href="{BASE}/">← DM Electricals home</a></nav>
</header>
<main>
  <h1>{escape(h1)}</h1>
  {body}
  <p><a href="{BASE}/#contact">Contact us — phone, WhatsApp &amp; quote form</a></p>
  {hub}
</main>
<footer>
  DM Electricals &amp; Installation · Mwihoko Road, Kasarani, Nairobi · Kenya · <a href="tel:+254799762232">0799 762 232</a>, <a href="tel:+254762748694">0762 748 694</a>
</footer>
</body>
</html>
"""


def write_pages() -> list[str]:
    urls: list[str] = [f"{BASE}/"]
    for slug, title, h1, meta, paras in SERVICES:
        path = f"services/{slug}.html"
        (ROOT / "services").mkdir(parents=True, exist_ok=True)
        (ROOT / path).write_text(page_html(path, title, h1, meta, paras, kind="service", slug=slug), encoding="utf-8")
        urls.append(f"{BASE}/{path}")
    for slug, title, h1, meta, paras in PRODUCTS:
        path = f"products/{slug}.html"
        (ROOT / "products").mkdir(parents=True, exist_ok=True)
        (ROOT / path).write_text(page_html(path, title, h1, meta, paras, kind="product", slug=slug), encoding="utf-8")
        urls.append(f"{BASE}/{path}")
    for slug, title, h1, meta, paras in AREAS:
        path = f"areas/{slug}.html"
        (ROOT / "areas").mkdir(parents=True, exist_ok=True)
        (ROOT / path).write_text(page_html(path, title, h1, meta, paras, kind="area", slug=slug), encoding="utf-8")
        urls.append(f"{BASE}/{path}")
    return urls


def write_sitemap(urls: list[str]) -> None:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for u in urls:
        lines.append("  <url>")
        lines.append(f"    <loc>{escape(u)}</loc>")
        lines.append(f"    <lastmod>{TODAY}</lastmod>")
        lines.append("    <changefreq>weekly</changefreq>")
        prio = "1.0" if u.rstrip("/") == BASE else "0.85"
        lines.append(f"    <priority>{prio}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    urls = write_pages()
    write_sitemap(urls)
    print(f"Generated {len(urls)} URLs in sitemap.xml")


if __name__ == "__main__":
    main()
