#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate SEO landing pages + sitemap.xml for DM Electricals static site."""

from __future__ import annotations

import json
import os
from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://dmelectricals.com"
TODAY = date.today().isoformat()

# (slug, title, h1, meta description, body paragraphs)
SERVICES: list[tuple[str, str, str, str, list[str]]] = [
    (
        "electrical-industrial-installation-nairobi",
        "Electrical & Industrial Installation Nairobi | DM Electricals",
        "Electrical & industrial installation in Nairobi",
        "Full electrical and industrial installations for homes, offices, and factories across Nairobi. Licensed team, Kenya Power standards, Mwihoko Road, Kasarani. Get a quote.",
        [
            "DM Electricals delivers complete electrical and industrial installations for residential estates, commercial buildings, and manufacturing facilities throughout Nairobi County and surrounding areas. Every project is planned with load calculations, quality materials, and safe cable routing.",
            "We work across Kasarani, Westlands, Ruaraka, Thika Road, Industrial Area, Roysambu, and the wider Nairobi region. Whether you need a new consumer unit, three-phase distribution, or full fit-out for a factory, our team follows ERC-aligned practices and clear documentation.",
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
            "We have completed projects in Roysambu, Kasarani, Ruaraka, Thika Road corridors, and other residential and commercial locations across Nairobi.",
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
            "Coverage includes Kasarani, Ruaraka, Westlands, Thika Road, Eastleigh, and apartment complexes across the city.",
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
            "Electrical emergencies can happen day or night. DM Electricals offers round-the-clock response for power failures, tripping breakers, burning smells, sparks, and dangerous faults across Nairobi.",
            "Our team aims to attend emergency calls quickly — often within an hour depending on location and traffic — from Kasarani and throughout Nairobi.",
            "Save our numbers: 0799 762 232 and 0762 748 694. Full contact and WhatsApp on our main website.",
        ],
    ),
]

PRODUCTS: list[tuple[str, str, str, str, list[str]]] = [
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

AREAS: list[tuple[str, str, str, str, list[str]]] = [
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
]


def page_html(path_from_root: str, title: str, h1: str, meta: str, paras: list[str]) -> str:
    canonical = f"{BASE}/{path_from_root}"
    body = "".join(f"<p>{escape(p)}</p>" for p in paras)
    ld = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": title,
        "description": meta,
        "url": canonical,
        "inLanguage": "en-KE",
        "isPartOf": {"@type": "WebSite", "name": "DM Electricals & Installation", "url": f"{BASE}/"},
    }
    ld_json = json.dumps(ld, ensure_ascii=False)
    return f"""<!DOCTYPE html>
<html lang="en-KE">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{escape(title)}</title>
<meta name="description" content="{escape(meta)}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{canonical}">
<link rel="icon" type="image/svg+xml" href="{BASE}/favicon.svg">
<link rel="icon" type="image/x-icon" href="{BASE}/favicon.ico" sizes="48x48 32x32 16x16">
<link rel="shortcut icon" href="{BASE}/favicon.ico">
<link rel="apple-touch-icon" href="{BASE}/favicon.ico">
<style>
body{{font-family:system-ui,-apple-system,sans-serif;line-height:1.65;max-width:720px;margin:0 auto;padding:2rem 1.25rem;color:#111827;background:#F8F8F8}}
a{{color:#8B1A2E;font-weight:600}}
h1{{font-size:1.5rem;line-height:1.25;margin-bottom:1rem}}
header{{margin-bottom:1.5rem;padding-bottom:1rem;border-bottom:1px solid #e5e7eb}}
footer{{margin-top:2rem;padding-top:1rem;border-top:1px solid #e5e7eb;font-size:0.875rem;color:#6b7280}}
</style>
<script type="application/ld+json">{ld_json}</script>
</head>
<body>
<header>
  <a href="{BASE}/">← DM Electricals home</a>
</header>
<main>
  <h1>{escape(h1)}</h1>
  {body}
  <p><a href="{BASE}/#contact">Contact us — phone, WhatsApp &amp; quote form</a></p>
</main>
<footer>
  DM Electricals &amp; Installation · Mwihoko Road, Kasarani, Nairobi · Kenya · 0799 762 232, 0762 748 694
</footer>
</body>
</html>
"""


def write_pages() -> list[str]:
    urls: list[str] = [f"{BASE}/"]
    for slug, title, h1, meta, paras in SERVICES:
        path = f"services/{slug}.html"
        (ROOT / "services").mkdir(parents=True, exist_ok=True)
        (ROOT / path).write_text(page_html(path, title, h1, meta, paras), encoding="utf-8")
        urls.append(f"{BASE}/{path}")
    for slug, title, h1, meta, paras in PRODUCTS:
        path = f"products/{slug}.html"
        (ROOT / "products").mkdir(parents=True, exist_ok=True)
        (ROOT / path).write_text(page_html(path, title, h1, meta, paras), encoding="utf-8")
        urls.append(f"{BASE}/{path}")
    for slug, title, h1, meta, paras in AREAS:
        path = f"areas/{slug}.html"
        (ROOT / "areas").mkdir(parents=True, exist_ok=True)
        (ROOT / path).write_text(page_html(path, title, h1, meta, paras), encoding="utf-8")
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
