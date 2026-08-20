# Demo Question Evaluation

Mode: grounded answers with gpt-4.1-mini

Retrieval coverage: 15/15 questions returned at least one evidence chunk.

Automated retrieval coverage is not a correctness judgment. A reviewer must verify relevance and the claim-to-citation-to-source chain.

## Document-defined evaluation contract

Questions 1-10 reproduce the required demo questions from the project description. Later questions are additional engineering checks and do not replace the official set.

### Official weighted rubric

| Category | Weight | Requirement | Reviewer score |
|---|---:|---|---:|
| Corpus and metadata | 20% | Documents are public, organized, and traceable to source URLs. | /20 |
| Search and retrieval | 20% | Semantic search returns relevant chunks with source information. | /20 |
| Entity and relation extraction | 20% | Outputs are understandable and useful for conservation knowledge organization. | /20 |
| LLM Wiki | 20% | Wiki pages consolidate evidence and link related entities. | /20 |
| Chatbot and demo | 20% | Chatbot provides useful, cited answers and avoids unsupported claims. | /20 |

Automated checks provide evidence for the rubric, but the final score remains a manual review.

## 1. What documents discuss aquatic invasive species?

Evaluation set: **Official document question**

Status: `structured_generated_pruned_refined`

Retrieval mode: `semantic`

### Retrieved evidence

- [DOC005, pp. 16-17] **Aquatic Invasive Species in the Chesapeake Bay Watershed** — with vested interests in invasive species man- agement in Chesapeake Bay and its drainage area. Documents produced by State and Federal partners that pertain at least in part to invasive species science or management were first reviewed with special attention to the mention of AIS-related management… [Source](https://pubs.usgs.gov/of/2020/1057/ofr20201057.pdf)
- [DOC005, p. 31] **Aquatic Invasive Species in the Chesapeake Bay Watershed** — one of proactive intervention to preclude AIS introductions and dissemination. It has long been recognized that the ecological and economic consequences of invasive species increase dramatically with time as the invasive species becomes established in a new habitat and niche (Cusack and others, 2009… [Source](https://pubs.usgs.gov/of/2020/1057/ofr20201057.pdf)
- [DOC009, pp. 1-3] **Aquatic Invasive Species Commission Report** — Aquatic Invasive Species Commission Report and Recommendations: Improving the Prevention, Eradication, Control and Mitigation of Aquatic Invasive Species (AIS) February 2023 AIS Commission: Improving the Prevention, Eradication, Control and Mitigation of Aquatic Invasive Species Report and Recommend… [Source](https://www.trcp.org/wp-content/uploads/2023/02/Aquatic-Invasive-Species-Report-3-28-2023.pdf)
- [DOC009, pp. 16-19] **Aquatic Invasive Species Commission Report** — Jeff Hill, University of Florida Dr. Jason Delborne, North Carolina State University Mike Greer, U.S. Army Corps of Engineers, ERDC Sarah LeSage, Michigan DEQ August 17, 2022: AIS Commission State, Regional, and Tribal Listening Session (Kenai, AK) The AIS Commission met in person and via video conf… [Source](https://www.trcp.org/wp-content/uploads/2023/02/Aquatic-Invasive-Species-Report-3-28-2023.pdf)
- [DOC010, pp. 2-4] **National Aquatic Invasive Species Outreach Workshop Summary Report** — province yielded new insights, especially from analysis of information sources and barriers for specific boating demographics and testing message framing, to improve aquatic invasive species (AIS) prevention, while reinforcing prior research. Echoing past surveys, many boaters felt a personal AIS pr… [Source](https://www.fws.gov/carp/sites/default/files/documents/2025-09/national-aquatic-invasive-species-outreach-workshop-summary-report.pdf)
- [DOC010, pp. 4-6] **National Aquatic Invasive Species Outreach Workshop Summary Report** — consistent application across all pathways has made it highly recognizable and rated highly in a statewide assessment. Illinois’ efforts can be a national model for creating and applying a campaign that may capture different audiences than national prevention brands. ○ Texas’ Protect the Lakes You L… [Source](https://www.fws.gov/carp/sites/default/files/documents/2025-09/national-aquatic-invasive-species-outreach-workshop-summary-report.pdf)
- [DOC006, pp. 1-3] **Aquatic Invasive Species Research Report** — Aquatic Invasive Species Research Report Section 1108 of WRDA 2018 Prepared by the Assistant Secretary of the Army for Civil Works June 2020 Aquatic Invasive Species Research: Addressing the Spread and Impacts of Aquatic Invasive Species This report describes ongoing and recently completed research … [Source](https://usace.contentdm.oclc.org/digital/api/collection/p16021coll5/id/35588/download)
- [DOC006, pp. 15-17] **Aquatic Invasive Species Research Report** — species research program reviews hosted by ERDC 2.3.4 Foster collaborative research and development with the Bureau of Reclamation and other Federal agencies to produce and infuse solutions for common invasive species challenges GOAL 3: CONTROL, ERADICATION AND RESTORATION MANAGEMENT Control and whe… [Source](https://usace.contentdm.oclc.org/digital/api/collection/p16021coll5/id/35588/download)

### Answer

The retrieved evidence supports:

- **Aquatic Invasive Species in the Chesapeake Bay Watershed** — Interviews and conversations with organizational representatives pertaining to aquatic invasive species science and management needs and priorities [DOC005, pp. 16-17]
- **Aquatic Invasive Species Commission Report** — and Recommendations: Improving the Prevention, Eradication, Control and Mitigation of Aquatic Invasive Species (AIS) February 2023 [DOC009, pp. 1-3]
- **Aquatic Invasive Species Research Report** — Aquatic Invasive Species Research: Addressing the Spread and Impacts of Aquatic Invasive Species This report describes ongoing and recently completed research activities performed by the U.S. Army Corps of Engineers (USACE) Engineer Research and Development Center (ERDC) related to the spread and impact of aquatic invasive species across the nation [DOC006, pp. 1-3]

### Manual review

- [ ] Retrieved chunks are relevant.
- [ ] Claims are supported by cited evidence.
- [ ] Document IDs and page numbers are correct.
- [ ] Unsupported claims are absent or the system abstained.
- Notes:

## 2. What agencies appear most often in the corpus?

Evaluation set: **Official document question**

Status: `deterministic`

Retrieval mode: `structured_entities`

### Retrieved evidence

- [DOC001, pp. 1-8] **Missouri State Wildlife Action Plan** — Missouri State Wildlife Action Plan Missouri Department of Conservation Conserving healthy fish, forests, and wildlife 2015 Missouri State Wildlife Action Plan 2015 Missouri is a national leader in fish, forest, and wildlife conservation due to Missouri citizens’ unique and proactive support of cons… [Source](https://www.mdc.mo.gov/sites/default/files/2020-04/SWAP_0.pdf)
- [DOC001, pp. 43-51] **Missouri State Wildlife Action Plan** — biodiversity: A comprehensive multiscaled approach. Island Press, Washington, DC. Matthews, J.W., G. Spyreas, and C.M. Long. 2015. A null model test of floristic quality assessment: are plant species coefficients of conservatism valid? Ecological Indicators 52: 1-7. McMurray, S.E., J.A. Fairman, A. … [Source](https://www.mdc.mo.gov/sites/default/files/2020-04/SWAP_0.pdf)
- [DOC001, pp. 36-37] **Missouri State Wildlife Action Plan** — finement of the COAs for the 2015 Plan. All partners who participated in development of the 2005 CWCS, the Missouri Forest Action Plan, or other recent coop- erative planning efforts were invited (see Appendix B, Partner Engagement Workshop Invitee List). Of the 58 partner agencies and organizations… [Source](https://www.mdc.mo.gov/sites/default/files/2020-04/SWAP_0.pdf)
- [DOC001, pp. 248-253] **Missouri State Wildlife Action Plan** — Coneflower 8 Eryngium yuccifolium Rattlesnake Master 9 Gentiana puberulenta Downy Gentian 7 Lilium michiganense Michigan Lily 10 Lilium philadelphicum Prairie Lily 9 Melanthium virginicum Bunch Flower 8 Platanthera lacera Ragged Fringed Orchid 8 Polytaenia nuttallii Prairie Parsley 10 Potentilla arg… [Source](https://www.mdc.mo.gov/sites/default/files/2020-04/SWAP_0.pdf)
- [DOC001, pp. 116-119] **Missouri State Wildlife Action Plan** — native grass - es and forbs that dominate these systems. Trees found on and near glades are often stunted and express poor development due to the shallow droughty soils and poor growing conditions. Therefore sandstone glades frequently exhibit patches of stunted shrub and tree species in areas with … [Source](https://www.mdc.mo.gov/sites/default/files/2020-04/SWAP_0.pdf)
- [DOC003, pp. 1-5] **North American Waterfowl Management Plan Update** — NORTH AMERICAN WATERFOWL MANAGEMENT PLAN EXPANDING the VISION Canada NAWMP Implementation Office Wildlife Conservation Branch Canadian Wildlife Service Environment Canada Place Vincent Massey, 3rd Floor 351 St. Joseph Boulevard Hull, Québec Canada K1A 0H3 Phone: (819) 997-2392 Fax: (819) 994-4445 E-… [Source](https://www.fws.gov/sites/default/files/documents/2024-04/1445.pdf)
- [DOC003, pp. 12-14] **North American Waterfowl Management Plan Update** — public, private, and common lands. • The Plan pioneered a partnership approach to conservation, which permeates all facets of Plan implementation. Looking back to 1986, those associated with the Plan should be congratulated for their record of exceptional contributions to habitat and species conserv… [Source](https://www.fws.gov/sites/default/files/documents/2024-04/1445.pdf)

### Answer

Using the extracted agency entities, ranked first by distinct document coverage and then by mention count:

- **U.S. Fish and Wildlife Service** — 133 extracted mentions across 19 documents. [DOC001, pp. 1-8]
- **U.S. Geological Survey** — 84 extracted mentions across 13 documents. [DOC001, pp. 43-51]
- **Missouri Department of Conservation** — 115 extracted mentions across 11 documents. [DOC001, pp. 1-8]
- **Ducks Unlimited** — 50 extracted mentions across 11 documents. [DOC001, pp. 36-37]
- **U.S. Environmental Protection Agency** — 34 extracted mentions across 11 documents. [DOC001, pp. 248-253]
- **U.S. Army Corps of Engineers** — 39 extracted mentions across 9 documents. [DOC001, pp. 116-119]
- **U.S. Department of the Interior** — 37 extracted mentions across 9 documents. [DOC003, pp. 1-5]
- **Convention on Wetlands** — 67 extracted mentions across 5 documents. [DOC003, pp. 12-14]

### Manual review

- [ ] Retrieved chunks are relevant.
- [ ] Claims are supported by cited evidence.
- [ ] Document IDs and page numbers are correct.
- [ ] Unsupported claims are absent or the system abstained.
- Notes:

## 3. What are the main conservation threats mentioned across the documents?

Evaluation set: **Official document question**

Status: `deterministic`

Retrieval mode: `structured_threats`

### Retrieved evidence

- [DOC001, pp. 27-29] **Missouri State Wildlife Action Plan** — and conservation partners will con- tinue to provide services statewide and constantly continue to explore valuable opportunities to con - serve Missouri’s natural communities and the spe- cies they support. The final selection criteria and COA maps for each habitat system are provided in the habita… [Source](https://www.mdc.mo.gov/sites/default/files/2020-04/SWAP_0.pdf)
- [DOC001, pp. 24-26] **Missouri State Wildlife Action Plan** — to 50 Great Places, author, Mike Leahy, describes the classifi - cation of Missouri into its primary ecological re - gions. Missouri is made up of four major ecolog- ical regions, or ecoregions—large geographic areas having distinctive topography, geology, soils, vegetation, and climate patterns (Fi… [Source](https://www.mdc.mo.gov/sites/default/files/2020-04/SWAP_0.pdf)
- [DOC001, pp. 30-31] **Missouri State Wildlife Action Plan** — grazing frequency reduce biodiversity by allowing dominant species to outcompete species adapted to disturbances that oc - curred regularly in the systems in which they evolved. Earlier successional systems such as grasslands, sa - vannas, woodlands and glades are most susceptible to this threat. Th… [Source](https://www.mdc.mo.gov/sites/default/files/2020-04/SWAP_0.pdf)

### Answer

Using extracted threat entities, ranked first by distinct document coverage and then by mention count:

- **Invasive species** — 202 extracted mentions across 22 documents. [DOC001, pp. 27-29]
- **Disease** — 89 extracted mentions across 19 documents. [DOC001, pp. 27-29]
- **Flooding** — 39 extracted mentions across 15 documents. [DOC001, pp. 24-26]
- **Climate change** — 115 extracted mentions across 14 documents. [DOC001, pp. 27-29]
- **Habitat loss** — 78 extracted mentions across 14 documents. [DOC001, pp. 27-29]
- **Pollution** — 155 extracted mentions across 12 documents. [DOC001, pp. 27-29]
- **Drought** — 30 extracted mentions across 11 documents. [DOC001, pp. 30-31]
- **Urban development** — 24 extracted mentions across 8 documents. [DOC001, pp. 27-29]

### Manual review

- [ ] Retrieved chunks are relevant.
- [ ] Claims are supported by cited evidence.
- [ ] Document IDs and page numbers are correct.
- [ ] Unsupported claims are absent or the system abstained.
- Notes:

## 4. What documents discuss wetlands or wetland management?

Evaluation set: **Official document question**

Status: `structured_generated_pruned_refined`

Retrieval mode: `semantic`

### Retrieved evidence

- [DOC002, pp. 10-13] **Missouri Wetland Program Plan** — Later Farm Bills strengthen this provision by making violators ineligible for farm program benefits. Page 10 | 20 The department supports Natural Resource Damage Assessment and Restoration (NRDAR) wetland restoration activities. X X X X X X The department’s NRDAR program along with USFWS support the… [Source](https://www.epa.gov/system/files/documents/2024-06/missouri_wetland-program-plan-20240117-cw.pdf)
- [DOC027, pp. 12-14] **Ramsar Resources** — VI.1 (1996), and the terms currently used in previous Ramsar guidelines and documents are shown here alongside those used in the MA. MA Ecosystem terms to apply in Ramsar guidelines and documents Terms used in various previous Ramsar guidelines and other documents Ecosystem Components: physical; che… [Source](https://web.archive.org/web/20240115041420id_/https://www.ramsar.org/sites/default/files/documents/library/manual6-2013-e.pdf)
- [DOC035, pp. 10-12] **DocumentCloud Wetland Search** — of the USEPA (United States Environmental Protection Agency). The Congress authorizes EPA and other federal agencies to write rules and regulations that explain the critic al details necessary to implement environmental laws.There are a number of sub agencies also which look after different aspects … [Source](https://s3.documentcloud.org/documents/3105657/Wetland-Protection.pdf)
- [DOC027, pp. 50-52] **Ramsar Resources** — of wetlands with potential for restoration. The Framework for Wetland Inventory, adopted by the COP in Resolution VIII.6 (2002) and the subsequent Framework for processes of detecting, reporting and responding to change in wetland ecological character (Resolution X.16, 2008; both in Handbook 15) pro… [Source](https://web.archive.org/web/20240115041420id_/https://www.ramsar.org/sites/default/files/documents/library/manual6-2013-e.pdf)
- [DOC022] **USFWS National Wetlands Inventory** — status of the nation’s wetland and deepwater habitats, as well as changes to these habitats over time. What We Do Our Services We produce and distribute maps and other geospatial data on American wetland and deepwater habitats, as well as monitor changes in these habitats through time. This informat… [Source](https://www.fws.gov/program/national-wetlands-inventory)
- [DOC001, pp. 17-20] **Missouri State Wildlife Action Plan** — to promote conservation action with partners. The CWCS was designed to be adaptive, and this is reflected in the current State Wildlife Action Plan (Plan). The Plan is a revision of Missouri’s CWCS; the new title reflects a change in terminology for these na- tionwide plans at a national level. In t… [Source](https://www.mdc.mo.gov/sites/default/files/2020-04/SWAP_0.pdf)
- [DOC002, pp. 1-3] **Missouri Wetland Program Plan** — Missouri Wetland Program Plan 2023 – 2028 Marsh Wetlands along the Missouri River Source: USGS Prepared by: Missouri Department of Natural Resources P.O. Box 176, Jefferson City, MO 65102 Phone: 800-361-4827 WQS@dnr.mo.gov Introduction Missouri’s wetlands are as diverse as the benefits they provide.… [Source](https://www.epa.gov/system/files/documents/2024-06/missouri_wetland-program-plan-20240117-cw.pdf)
- [DOC001, pp. 147-150] **Missouri State Wildlife Action Plan** — blackbird (Euphagus carolinus) ✦ Least bittern (Ixobrychus exilis) ✦ Black-crowned night-heron (Nycticorax nycticorax) ✦ Sora (Porzana carolina) ✦ King rail (Rallus elegans) ✦ Virginia rail (Rallus limicola) Mammals Characteristic: Rice rat (Oryzomys palustris) ✦ Cotton mouse (Peromyscus gossypinus)… [Source](https://www.mdc.mo.gov/sites/default/files/2020-04/SWAP_0.pdf)

### Answer

The retrieved evidence supports:

- **Missouri Wetland Program Plan** — The department will participate in, and facilitate, the review and approval of wetland mitigation banking and in-lieu fee program instruments; including, review and approval of new wetland mitigation plans for each additional site once instrument is established [DOC002, pp. 10-13]
- **DocumentCloud Wetland Search** — Technical Tools for the Management of Lake/Wetland Management ... Adoption of floodplains, stream buffer or “Hydric Soil Ordinance” that can protect or act as a buffer zone between the water body and the terrestrial ecosystem [DOC035, pp. 10-12]
- **USFWS National Wetlands Inventory** — We produce and distribute maps and other geospatial data on American wetland and deepwater habitats, as well as monitor changes in these habitats through time [DOC022]

### Manual review

- [ ] Retrieved chunks are relevant.
- [ ] Claims are supported by cited evidence.
- [ ] Document IDs and page numbers are correct.
- [ ] Unsupported claims are absent or the system abstained.
- Notes:

## 5. What public documents mention waterfowl conservation?

Evaluation set: **Official document question**

Status: `deterministic`

Retrieval mode: `structured_cooccurrence`

### Retrieved evidence

- [DOC014, pp. 1-4] **Habitat Matters** — HabitatMatters 2025 Canadian N A W M P Report September 2025 nawmp.wetlandnetwork.ca “Northward Bound – Greater Scaup” from the 2025 Canadian Wildlife Habitat Conservation Stamp series. Artist: Ken Ferris North American Waterfowl Management Plan —— Pl an nord-américain de ge stion de la sauvagine ——… [Source](https://publications.gc.ca/collections/collection_2025/eccc/CW71-8-2025-eng.pdf)
- [DOC003, pp. 1-5] **North American Waterfowl Management Plan Update** — NORTH AMERICAN WATERFOWL MANAGEMENT PLAN EXPANDING the VISION Canada NAWMP Implementation Office Wildlife Conservation Branch Canadian Wildlife Service Environment Canada Place Vincent Massey, 3rd Floor 351 St. Joseph Boulevard Hull, Québec Canada K1A 0H3 Phone: (819) 997-2392 Fax: (819) 994-4445 E-… [Source](https://www.fws.gov/sites/default/files/documents/2024-04/1445.pdf)
- [DOC027, pp. 8-9] **Ramsar Resources** — the southern shore of the Caspian Sea. Thus, though nowadays the name of the Convention is usually written “Convention on Wetlands (Ramsar, Iran, 1971)”, it has come to be known popularly as the “Ramsar Convention”. Ramsar is the first of the modern global intergovernmental treaties on the conservat… [Source](https://web.archive.org/web/20240115041420id_/https://www.ramsar.org/sites/default/files/documents/library/manual6-2013-e.pdf)
- [DOC013, pp. 5-7] **State Wildlife Action Plans Report with State Summaries** — wildlife to decline and react to problems with expensive, last-ditch recovery efforts, or we can act now to prevent wildlife from becoming endangered. Taken together, the wildlife action plans represent the right decision to take action before wildlife recovery becomes costly and controversial. Work… [Source](https://www.fishwildlife.org/application/files/6415/1856/1631/StateWildlifeActionPlansReportwithStateSummaries.pdf)
- [DOC034, pp. 81-84] **DocumentCloud Conservation Search** — 5 million Canadians in related farm supply, processing, distribution and retail businesses—the agri-food industry. Sales of pri- mary agricultural products alone amount to $22 billion annually. The quality of soil, water and air; the impact of agricultural activities on wildlife habitat and water qu… [Source](https://s3.documentcloud.org/documents/6563087/Canada-s-Green-Plan-1990.pdf)
- [DOC001, pp. 140-145] **Missouri State Wildlife Action Plan** — by strict defini- tion, bottomland forests and wet prairies are consid - ered in the forest and prairie sections, respectively. In the Ozarks sinkhole ponds can act as ephemeral wet - lands or support subtype communities of emergent marsh, forested swamp, and shrub swamp. Wetland plant, fish, and wi… [Source](https://www.mdc.mo.gov/sites/default/files/2020-04/SWAP_0.pdf)
- [DOC015, pp. 1-2] **Missouri Conservation Report** — MISSOURI STATE REPORT May 6, 2025 Jason Sumners, Director Missouri Department of Conservation 2901 West Truman Blvd. Jefferson City, MO 65102 Financial Update The Fiscal Year (FY) 2025 budget for the Missouri Department of Conservation (MDC) continues to represent less than 1 percent of the total st… [Source](https://irp.cdn-website.com/92033df0/files/uploaded/mo_rpt25.pdf)
- [DOC004, pp. 1-3] **NAWMP Value Proposition** — North American Waterfowl Management Plan A World-Class Opportunity to Help Conserve Today’s Natural Resources for Tomorrow The North American Waterfowl Management Plan is an international strategy for conserving migratory waterfowl and their habitats throughout the continent. It is one of the most s… [Source](https://nawmp.org/sites/default/files/2022-03/NAWMP%20Value%20Prop%20Abbreviated%20version%202016%20FINAL_sm.pdf)
- [DOC020, pp. 26-28] **MDC Conservation Resources** — care of nature Fiscal Year Comparison FY2022 to FY2023 Change Land Conservation & Partnerships 24 HB Section(s): 6.605 1a. What strategic priority does this program address? Take care of nature 1b. What does this program do? PROGRAM DESCRIPTION Department of Conservation Program Name: Fish & Wildlif… [Source](https://mdc.mo.gov/sites/default/files/2022-06/FY23IEPbook.pdf)
- [DOC021] **Ducks Unlimited Conservation Resources** — Migration Map Volunteer Location: TN Change View State Page Ducks Unlimited Conservation Waterfowl, Wildlife and People Need Wetlands Ducks Unlimited has conserved more than 20 million acres of wetlands and other waterfowl habitats across North America​ Why Wetlands Matter More than half of North Am… [Source](https://www.ducks.org/conservation)
- [DOC016] **MDC Annual Review FY2024** — and Tribal Forestry. Wildfire Going into FY24, Missouri was experiencing effects of drought conditions, which continued through May. Missouri received significant rainfall in June, relieving most of the drought conditions. Before rainfall arrived, MDC staff and partnering fire departments experience… [Source](https://mdc.mo.gov/magazines/missouri-conservationist/2025-01/annual-review-fiscal-year-july-1-2023-june-30-2024)
- [DOC017] **MDC Annual Review FY2023** — partnership is made up of agencies and organizations that are committed to total elimination of feral hogs from Missouri’s landscape. In 2020, the partnership established a unified incident command system to manage feral hog elimination efforts in the state. Since 2016, the partnership has eliminate… [Source](https://mdc.mo.gov/magazines/missouri-conservationist/2024-01/annual-review-fiscal-year-2023)
- [DOC026] **USFWS Migratory Birds Program** — supporting one of the nation's oldest and most successful conservation programs - YOU have an opportunity to play a crucial role in bird conservation. Neotropical Migratory Bird Conservation Act (NMBCA) Grants The Neotropical Migratory Bird Conservation Act (NMBCA) Grant Program funds projects promo… [Source](https://www.fws.gov/program/migratory-birds)
- [DOC031, pp. 8-9] **DocumentCloud Public Search** — Winnebago Lake Winnebago in Fond Du Lac County, Wisconsin, is the host of many national fishing tournaments. When residents got tired of seeing summer algae blooms (sometimes so bad that they covered the entire lake, creating a foul smell) they formed the Lake Winnebago East Priority Water- shed Pro… [Source](https://s3.documentcloud.org/documents/24223250/epa-2000-report-on-americas-water-resources.pdf)
- [DOC032, pp. 6-7] **DocumentCloud Environment Project Search** — six global agreements 4 relating to nature and the protection of the global environment are demonstrably on track to be met. For nearly one third of the goals of these conventions there has been little or no progress towards them or, instead, movement away from them. C2 Nature is essential for achie… [Source](https://s3.documentcloud.org/documents/5990576/Summary-for-Policymakers-IPBES-Global-Assessment.pdf)

### Answer

An explicit corpus scan found these documents with both “waterfowl” and “conservation” in the same stored evidence chunk:

- **Habitat Matters** — [DOC014, pp. 1-4]
- **North American Waterfowl Management Plan Update** — [DOC003, pp. 1-5]
- **Ramsar Resources** — [DOC027, pp. 8-9]
- **State Wildlife Action Plans Report with State Summaries** — [DOC013, pp. 5-7]
- **DocumentCloud Conservation Search** — [DOC034, pp. 81-84]
- **Missouri State Wildlife Action Plan** — [DOC001, pp. 140-145]
- **Missouri Conservation Report** — [DOC015, pp. 1-2]
- **NAWMP Value Proposition** — [DOC004, pp. 1-3]
- **MDC Conservation Resources** — [DOC020, pp. 26-28]
- **Ducks Unlimited Conservation Resources** — [DOC021]
- **MDC Annual Review FY2024** — [DOC016]
- **MDC Annual Review FY2023** — [DOC017]
- **USFWS Migratory Birds Program** — [DOC026]
- **DocumentCloud Public Search** — [DOC031, pp. 8-9]
- **DocumentCloud Environment Project Search** — [DOC032, pp. 6-7]

### Manual review

- [ ] Retrieved chunks are relevant.
- [ ] Claims are supported by cited evidence.
- [ ] Document IDs and page numbers are correct.
- [ ] Unsupported claims are absent or the system abstained.
- Notes:

## 6. What is the relationship between invasive carp and aquatic habitat management?

Evaluation set: **Official document question**

Status: `structured_generated_pruned`

Retrieval mode: `semantic`

### Retrieved evidence

- [DOC006, pp. 3-4] **Aquatic Invasive Species Research Report** — from Navigation to Flood Risk Management to Environmental Stewardship, is impacted by AIS. Nearly every aquatic ecosystem restoration project undertaken by USACE involves some form of invasive species consideration – whether species removal prior to restoration or management thereafter to prevent ne… [Source](https://usace.contentdm.oclc.org/digital/api/collection/p16021coll5/id/35588/download)
- [DOC001, pp. 170-172] **Missouri State Wildlife Action Plan** — a stream system. Connectivity Loss Streams rely on their watershed connections that run horizontally into the riparian area and floodplains, longitudinally up and down channels, and vertically between the channel bed and the water table. Com - mon causes of horizontal connectivity loss occur in floo… [Source](https://www.mdc.mo.gov/sites/default/files/2020-04/SWAP_0.pdf)
- [DOC016] **MDC Annual Review FY2024** — Assessment and Monitoring Strategic Initiative, which focuses resources on developing tools to assess and monitor the effectiveness of conservation actions within priority geographies. This work is being accomplished by developing achievable and desired future conditions using the Missouri River Hil… [Source](https://mdc.mo.gov/magazines/missouri-conservationist/2025-01/annual-review-fiscal-year-july-1-2023-june-30-2024)
- [DOC015, pp. 2-3] **Missouri Conservation Report** — 2001, behind only 2015 at 4,449 birds. Brown-headed Nuthatch. MDC and partners continued Brown-headed Nuthatch reintroduction efforts in the Missouri Ozarks. In 2020 and 2021, MDC released 102 birds to the U.S. Forest Service’s Mark Twain National Forest as part of a pilot effort to achieve holistic… [Source](https://irp.cdn-website.com/92033df0/files/uploaded/mo_rpt25.pdf)
- [DOC012, pp. 16-18] **Invasive Carp Strategic Science Plan** — Our research supports assessing the efficacy and registration of these tech- nologies for use in natural resource management. As new technologies and approaches are developed, the USGS will evaluate their practicality and utility. We acknowl- edge that there can be public concern regarding the risks… [Source](https://www.govinfo.gov/content/pkg/GOVPUB-I19-PURL-gpo224710/pdf/GOVPUB-I19-PURL-gpo224710.pdf)
- [DOC012, pp. 11-12] **Invasive Carp Strategic Science Plan** — prevention and management. USGS research also supports efforts of Federal management partners, such as the invasive carp subbasin partnerships (that is, the inva- sive carp partnerships of the Upper Mississippi River; Lower Mississippi River; Missouri River; Ohio River; Tennessee and Cumberland Rive… [Source](https://www.govinfo.gov/content/pkg/GOVPUB-I19-PURL-gpo224710/pdf/GOVPUB-I19-PURL-gpo224710.pdf)

### Answer

The retrieved evidence supports:

- USACE operates electric dispersal barriers in the Chicago Sanitary and Ship Canal to prevent interbasin transfer of invasive fish, particularly Asian carp, between the Mississippi River and Great Lakes basins. [DOC006, pp. 3-4]
- An invasive carp removal project on the Lamine River extracted 43,000 lbs. of silver and bighead carp in a 2-week effort to inform on commercial fishing potential for the tributary of the Missouri River. [DOC015, pp. 2-3]

### Manual review

- [ ] Retrieved chunks are relevant.
- [ ] Claims are supported by cited evidence.
- [ ] Document IDs and page numbers are correct.
- [ ] Unsupported claims are absent or the system abstained.
- Notes:

## 7. Which documents are most relevant to Missouri conservation planning?

Evaluation set: **Official document question**

Status: `structured_generated_pruned_narrowed_refined`

Retrieval mode: `semantic`

### Retrieved evidence

- [DOC001, pp. 35-36] **Missouri State Wildlife Action Plan** — Plan at intervals not to exceed ten years. This State Wildlife Action Plan (Plan) is a revision of the Comprehensive Wildlife Conservation Strategy (CWCS) completed in 2005. The CWCS used all the information acquired in the prior 30 years to identify a set of Conservation Opportunity Areas (COAs) to… [Source](https://www.mdc.mo.gov/sites/default/files/2020-04/SWAP_0.pdf)
- [DOC002, pp. 1-3] **Missouri Wetland Program Plan** — Missouri Wetland Program Plan 2023 – 2028 Marsh Wetlands along the Missouri River Source: USGS Prepared by: Missouri Department of Natural Resources P.O. Box 176, Jefferson City, MO 65102 Phone: 800-361-4827 WQS@dnr.mo.gov Introduction Missouri’s wetlands are as diverse as the benefits they provide.… [Source](https://www.epa.gov/system/files/documents/2024-06/missouri_wetland-program-plan-20240117-cw.pdf)
- [DOC018] **MDC Annual Review FY2021** — Water, Urban League of Metro St. Louis, St. Louis County Police Department, and many others to participate in the “Clean Up, Build Up” project to help clean up the trash, debris, and overgrowth of invasive species in the underserved community of Castle Point in North St. Louis County. Several 40-yar… [Source](https://mdc.mo.gov/magazines/missouri-conservationist/2023-01/annual-review)
- [DOC019] **MDC Management Plans** — MDC Management Plans In This Section Masthead Cards Body Browse our strategic plans for managing Missouri's fish, forests, and wildlife. + see more - show less Title Comprehensive Plans Link or File Media Fishing for the Future 818.87 KB Description Our plan for angler recruitment and retention in M… [Source](https://mdc.mo.gov/wildlife/mdc-management-plans)
- [DOC001, pp. 27-29] **Missouri State Wildlife Action Plan** — and conservation partners will con- tinue to provide services statewide and constantly continue to explore valuable opportunities to con - serve Missouri’s natural communities and the spe- cies they support. The final selection criteria and COA maps for each habitat system are provided in the habita… [Source](https://www.mdc.mo.gov/sites/default/files/2020-04/SWAP_0.pdf)
- [DOC018] **MDC Annual Review FY2021** — key conservation opportunities and prioritization in community conservation, public access to nature, climate change resiliency, and ecosystem services. The Missouri CCS was approved in February 2022. This is the first time a state has combined these documents into a single framework. Missouri’s pla… [Source](https://mdc.mo.gov/magazines/missouri-conservationist/2023-01/annual-review)
- [DOC013, pp. 139-141] **State Wildlife Action Plans Report with State Summaries** — with the Ozark Highlands – a region of forests and woodlands that still supports much native wildlife. The northern plains were formerly prairies and savannas dissected with wooded streams. To- day, much of north Missouri is used for crop agriculture and cattle graz- ing. The western border of Misso… [Source](https://www.fishwildlife.org/application/files/6415/1856/1631/StateWildlifeActionPlansReportwithStateSummaries.pdf)
- [DOC013, pp. 140-143] **State Wildlife Action Plans Report with State Summaries** — ” –Roger Still, Executive Direc- tor, Audubon Missouri 141 Highlight habitats Wildlife Issues Actions Prairie: Golden Grasslands Conservation Opportunity Area Ownership: Mix of public/private • Prairie mole cricket • Grassland Crayfi sh • Northern crawfi sh frog • Bullsnake • Greater prairie- chicke… [Source](https://www.fishwildlife.org/application/files/6415/1856/1631/StateWildlifeActionPlansReportwithStateSummaries.pdf)

### Answer

The retrieved evidence supports:

- **Missouri State Wildlife Action Plan** — This State Wildlife Action Plan (Plan) is a revision of the Comprehensive Wildlife Conservation Strategy (CWCS) completed in 2005. The CWCS used all the information acquired in the prior 30 years to identify a set of Conservation Opportunity Areas (COAs) to support and conserve viable populations of all wild - life and the habitat systems on which they depend [DOC001, pp. 35-36]
- **MDC Management Plans** — Browse our strategic plans for managing Missouri's fish, forests, and wildlife [DOC019]
- **State Wildlife Action Plans Report with State Summaries** — Missouri’s Comprehensive Wildlife Strategy promotes management that benefi ts all wildlife, rather than targeting sin- gle species. The strategy identifi es 33 Conservation Opportunity Areas in which management strategies will conserve both wildlife populations and the natural systems on which they depend [DOC013, pp. 139-141]

### Manual review

- [ ] Retrieved chunks are relevant.
- [ ] Claims are supported by cited evidence.
- [ ] Document IDs and page numbers are correct.
- [ ] Unsupported claims are absent or the system abstained.
- Notes:

## 8. Generate a short cited summary of wetland conservation evidence in the corpus.

Evaluation set: **Official document question**

Status: `deterministic`

Retrieval mode: `structured_wetland_summary`

### Retrieved evidence

- [DOC001, pp. 249-253] **Missouri State Wildlife Action Plan** — the whole prairie area) of all conservative plant species noted taken as a whole? For sites with 10+ conservative species, consider the abundance of all the species (in aggregate) up to the total 53 possible. Abundance Ranking Points Abundant or very frequently observed(>50 % of the area) 14 Frequen… [Source](https://www.mdc.mo.gov/sites/default/files/2020-04/SWAP_0.pdf)
- [DOC001, pp. 248-253] **Missouri State Wildlife Action Plan** — Coneflower 8 Eryngium yuccifolium Rattlesnake Master 9 Gentiana puberulenta Downy Gentian 7 Lilium michiganense Michigan Lily 10 Lilium philadelphicum Prairie Lily 9 Melanthium virginicum Bunch Flower 8 Platanthera lacera Ragged Fringed Orchid 8 Polytaenia nuttallii Prairie Parsley 10 Potentilla arg… [Source](https://www.mdc.mo.gov/sites/default/files/2020-04/SWAP_0.pdf)
- [DOC027, pp. 9-10] **Ramsar Resources** — Article 2.1 provides that wetlands to be included in the Ramsar List of internationally important wetlands: “may incorporate riparian and coastal zones adjacent to the wetlands, and islands or bodies of marine water deeper than six metres at low tide lying within the wetlands”. Five major wetland ty… [Source](https://web.archive.org/web/20240115041420id_/https://www.ramsar.org/sites/default/files/documents/library/manual6-2013-e.pdf)
- [DOC027, pp. 95-98] **Ramsar Resources** — the ecological functions of wetlands (2002). www.ramsar.org/pdf/guide/guide-allocation.pdf; Handbook 8, www.ramsar. org/pdf/lib/hbk4-08.pdf. The Convention on Wetlands (Ramsar, Iran, 1971) 94 Wetland losses: An Integrated Framework and guidelines for avoiding, mitigating and compensating for wetland… [Source](https://web.archive.org/web/20240115041420id_/https://www.ramsar.org/sites/default/files/documents/library/manual6-2013-e.pdf)
- [DOC024] **USGS Wetland and Aquatic Research Center** — Celebrating American Wetlands Month with USGS Wetland Science Dive into the wonderful world of wetland science as we celebrate American Wetlands Month! Explore WARC Wetland Science USGS WARC Leads Offshore Expedition off Aleutian Islands This effort will enhance our understanding of the Aleutian Isl… [Source](https://www.usgs.gov/centers/wetland-and-aquatic-research-center)
- [DOC002, pp. 6-8] **Missouri Wetland Program Plan** — (EDH) dataset to update and replace the National Hydrography Dataset (NHD) that has become a static product. This will be incorporated in the United States Geological Survey 3D Hydrography Program (USGS 3DHP) and be tied into the National Map of geospatial datasets used for flood modeling, natural r… [Source](https://www.epa.gov/system/files/documents/2024-06/missouri_wetland-program-plan-20240117-cw.pdf)

### Answer

A short evidence-based summary of wetland conservation in the corpus:

- The Missouri State Wildlife Action Plan uses vegetation, animal-species, and disturbance metrics to calculate a Community Health Index for assessing wetland condition. [DOC001, pp. 249-253], [DOC001, pp. 248-253]
- Ramsar guidance describes major wetland types, emphasizes their high biological productivity and biodiversity value, and calls for wise use that maintains ecological character. [DOC027, pp. 9-10], [DOC027, pp. 95-98]
- The USGS Wetland and Aquatic Research Center provides research, monitoring, and tools for wetland management and restoration. [DOC024]
- The Missouri Wetland Program Plan documents collaboration on wetland inventories, community health indices, hydrologic monitoring, research, and restoration planning. [DOC002, pp. 6-8]

### Manual review

- [ ] Retrieved chunks are relevant.
- [ ] Claims are supported by cited evidence.
- [ ] Document IDs and page numbers are correct.
- [ ] Unsupported claims are absent or the system abstained.
- Notes:

## 9. What wiki pages were generated for species, habitats, threats, and agencies?

Evaluation set: **Official document question**

Status: `deterministic`

Retrieval mode: `wiki_inventory`

### Retrieved evidence

- [DOC001, pp. 126-129] **Missouri State Wildlife Action Plan** — serrata) ✦ Slender-fingered cave isopod (Caecidotea stiladactyla) ✦ Stygian cave isopod (Caecidotea stygia) ✦ Cave crayfish (Cambarus aculabrum) ✦ Bristly cave crayfish (Cambarus setosus) ✦ Yeatman’s groundwater copepod Diacyclops yeatmani) ✦ Meek’s crayfish (Orconectes meeki meeki) ✦ Caney Mountain… [Source](https://www.mdc.mo.gov/sites/default/files/2020-04/SWAP_0.pdf)
- [DOC009, pp. 1-3] **Aquatic Invasive Species Commission Report** — Aquatic Invasive Species Commission Report and Recommendations: Improving the Prevention, Eradication, Control and Mitigation of Aquatic Invasive Species (AIS) February 2023 AIS Commission: Improving the Prevention, Eradication, Control and Mitigation of Aquatic Invasive Species Report and Recommend… [Source](https://www.trcp.org/wp-content/uploads/2023/02/Aquatic-Invasive-Species-Report-3-28-2023.pdf)
- [DOC012, pp. 22-24] **Invasive Carp Strategic Science Plan** — impractical, and funding will be diverted to other more promising avenues of research. • Early detection and surveillance.—There are criti- cal needs for invasive carp research focused on early detection of carp invasion and on carp reproductive success in new areas. The USGS will continue to inform… [Source](https://www.govinfo.gov/content/pkg/GOVPUB-I19-PURL-gpo224710/pdf/GOVPUB-I19-PURL-gpo224710.pdf)
- [DOC014, pp. 28-31] **Habitat Matters** — these birds forage, they stir up nutrients, control algae and disperse seeds, contributing to the health of this biodiversity hotspot. Habitat Matters 272025 Canadian North American Waterfowl Management Plan Report “There’s also a critical benefit that’s not obvious,” said Mark Francis, D U C’s mana… [Source](https://publications.gc.ca/collections/collection_2025/eccc/CW71-8-2025-eng.pdf)
- [DOC001, pp. 149-153] **Missouri State Wildlife Action Plan** — achieve stream-floodplain-watershed conservation and restoration in Missouri by establishing an interdis- ciplinary statewide task force with participation from agencies and partners directly involved with stream-floodplain-watershed management. ✦ Improve management of wetland complexes to benefit w… [Source](https://www.mdc.mo.gov/sites/default/files/2020-04/SWAP_0.pdf)
- [DOC027, pp. 24-26] **Ramsar Resources** — a series of amendments to Articles 6 and 7 that were accepted at an Extraordinary Conference of the Contracting Parties held in Regina, Canada, in 1987. These did not affect the basic substantive principles of the Convention, but related to its operation – briefly, the amendments defined the powers … [Source](https://web.archive.org/web/20240115041420id_/https://www.ramsar.org/sites/default/files/documents/library/manual6-2013-e.pdf)
- [DOC005, pp. 13-14] **Aquatic Invasive Species in the Chesapeake Bay Watershed** — A report of partner agencies’ needs and priorities related to aquatic invasive species (AIS) science was identified as an informational gap; a report would help to further development of the science program related to aquatic animal health and habitat. This objective was addressed through review of … [Source](https://pubs.usgs.gov/of/2020/1057/ofr20201057.pdf)
- [DOC033, pp. 71-74] **DocumentCloud Water Quality Search** — of life through technology and prioritizes investments for the most vulnerable Develop and expand partnerships for education, training, and outreach efforts for residents around climate action and sustainability Make the Cleveland Climate Action Fund financially sustainable and increase impact a b c… [Source](https://s3.documentcloud.org/documents/4911870/Cleveland-Climate-Action-Plan-2018.pdf)
- [DOC001, pp. 83-85] **Missouri State Wildlife Action Plan** — ✦ Plains spotted skunk (Spilogale putorius interrupta) Characteristic: Southeastern bat (Myotis austroriparius) ✦ Indiana bat (Myotis sodalis) ✦ Golden mouse (Ochrotomys nuttalli) ✦ Black bear (Ursus americanus) Species of Greatest Conservation Need Timber Rattlesnake Prothonotary Warbler Black Bear… [Source](https://www.mdc.mo.gov/sites/default/files/2020-04/SWAP_0.pdf)
- [DOC017] **MDC Annual Review FY2023** — the state of wetland conservation in Missouri. A Missouri Grasslands Summit is being planned for April 2024 with the same objective as the wetlands summit. Missouri Comprehensive Conservation Strategy During this past year, 19 regional Comprehensive Conservation Strategy (CCS) trainings were provide… [Source](https://mdc.mo.gov/magazines/missouri-conservationist/2024-01/annual-review-fiscal-year-2023)

### Answer

The generated wiki inventory contains:

- **Species:** Bighead carp [DOC009, pp. 1-3]; Hydrilla [DOC005, pp. 13-14]; Invasive carp [DOC012, pp. 22-24]
- **Habitats:** Forest [DOC014, pp. 28-31]; Marsh [DOC001, pp. 149-153]; Wetland [DOC027, pp. 24-26]
- **Threats:** Climate change [DOC033, pp. 71-74]; Disease [DOC001, pp. 83-85]; Invasive species [DOC017]
- **Agencies:** Missouri Department of Conservation [DOC001, pp. 126-129]; U.S. Fish and Wildlife Service [DOC009, pp. 1-3]; U.S. Geological Survey [DOC012, pp. 22-24]

### Manual review

- [ ] Retrieved chunks are relevant.
- [ ] Claims are supported by cited evidence.
- [ ] Document IDs and page numbers are correct.
- [ ] Unsupported claims are absent or the system abstained.
- Notes:

## 10. What important questions remain unanswered by this corpus?

Evaluation set: **Official document question**

Status: `deterministic`

Retrieval mode: `structured_explicit_gaps`

### Retrieved evidence

- [DOC013, pp. 55-57] **State Wildlife Action Plans Report with State Summaries** — eagles and burbots. Here, too, live globally signifi cant populations of species such as the saltmarsh sharp-tailed sparrow and the blue-winged warbler. Ancient species such as the horseshoe Connecticut Comprehensive Wildlife Conservation Strategy “This is an historic opportunity to help reverse the… [Source](https://www.fishwildlife.org/application/files/6415/1856/1631/StateWildlifeActionPlansReportwithStateSummaries.pdf)
- [DOC001, pp. 31-33] **Missouri State Wildlife Action Plan** — climate. ✦ Current major stressors and threats to forest eco - systems in the region include the following, which will be influenced and interact with a changing climate with uncertain results: ✧ Fragmentation and loss of forest cover ✧ Loss of historical fire regime in fire-adapted systems ✧ Nonnat… [Source](https://www.mdc.mo.gov/sites/default/files/2020-04/SWAP_0.pdf)
- [DOC003, pp. 30-31] **North American Waterfowl Management Plan Update** — over the last four decades. Annual winter surveys that were used to index the size of the black duck population estimated an average of 491,000 birds during the 1960s, falling to 285,000 during the 1990s. Although black ducks have declined in both the Atlantic and Mississippi Flyways, the proportion… [Source](https://www.fws.gov/sites/default/files/documents/2024-04/1445.pdf)
- [DOC009, pp. 12-15] **Aquatic Invasive Species Commission Report** — tural resources. Congress should expand USFWS grants to states and tribes to support contract fishing, including per -pound subsidies for invasive carp harvest and other harvest of AIS. Additional funding could support research and science-supported bounty programs for AIS harvest, while prioritizin… [Source](https://www.trcp.org/wp-content/uploads/2023/02/Aquatic-Invasive-Species-Report-3-28-2023.pdf)
- [DOC018] **MDC Annual Review FY2021** — effort, 56 birds were moved in August 2021 from Arkansas to two sites in the Mark Twain National Forest pineries south of Fremont. Between 2020 and 2021, a total of 102 nuthatches were released in Missouri. Partners at the University of Missouri, U.S. Forest Service, U.S. Fish and Wildlife Service, … [Source](https://mdc.mo.gov/magazines/missouri-conservationist/2023-01/annual-review)
- [DOC032, pp. 12-13] **DocumentCloud Environment Project Search** — declines in nature, emphasizing declines in biodiversity, that have been and are being caused by direct and indirect drivers of change. The direct drivers (land/sea use change; direct exploitation of organisms; climate change; pollution; and invasive alien species) 5 result from an array of underlyi… [Source](https://s3.documentcloud.org/documents/5990576/Summary-for-Policymakers-IPBES-Global-Assessment.pdf)

### Answer

The sources explicitly identify these uncertainties or information needs:

- **State Wildlife Action Plans Report with State Summaries:** A lack of information on the status of many GCN species, especially invertebrates, confi rms the need for targeted research so that these species can be addressed in future revisions of this Strategy. [DOC013, pp. 55-57]
- **Missouri State Wildlife Action Plan:** Many potential impacts on wildlife and their habitats remain unknown. [DOC001, pp. 31-33]
- **North American Waterfowl Management Plan Update:** While few data currently exist on these populations, information gaps are being addressed. [DOC003, pp. 30-31]
- **Aquatic Invasive Species Commission Report:** While long-term impacts and efficacy of AIS harvest markets remain somewhat uncertain, innovative control strategies have brought new stakeholders to the table in combatting established AIS. [DOC009, pp. 12-15]
- **MDC Annual Review FY2021:** SPR models can use data streams — harvest data and brood survey results — to estimate vital rates and abundance but need additional data to decrease the uncertainty around those estimates. [DOC018]
- **DocumentCloud Environment Project Search:** The proportion of insect species threatened with extinction is a key uncertainty, but available evidence supports a tentative estimate of 10 per cent (established but incomplete) {2.2.5.2.4}. [DOC032, pp. 12-13]

### Manual review

- [ ] Retrieved chunks are relevant.
- [ ] Claims are supported by cited evidence.
- [ ] Document IDs and page numbers are correct.
- [ ] Unsupported claims are absent or the system abstained.
- Notes:

## 11. How do conservation threats described for Missouri compare with threats in the Chesapeake Bay watershed?

Evaluation set: **Additional engineering question**

Status: `coverage_abstention`

Retrieval mode: `semantic`

### Retrieved evidence

- [DOC016] **MDC Annual Review FY2024** — Assessment and Monitoring Strategic Initiative, which focuses resources on developing tools to assess and monitor the effectiveness of conservation actions within priority geographies. This work is being accomplished by developing achievable and desired future conditions using the Missouri River Hil… [Source](https://mdc.mo.gov/magazines/missouri-conservationist/2025-01/annual-review-fiscal-year-july-1-2023-june-30-2024)
- [DOC005, pp. 22-23] **Aquatic Invasive Species in the Chesapeake Bay Watershed** — drainage area and hence the Chesapeake Bay watershed (U.S. Department of Agriculture Natural Resources Conservation Service West Virginia, 2019). Management Although AIS interests within West Virginia are heavily focused upon invasive carp and other species of concern in the Ohio River drainage area… [Source](https://pubs.usgs.gov/of/2020/1057/ofr20201057.pdf)
- [DOC005, pp. 31-33] **Aquatic Invasive Species in the Chesapeake Bay Watershed** — AIS presence in the region. Some jurisdictions in the region, including New York State and the Commonwealth of Pennsylvania, alternatively utilize the iMAPInvasives strategic management tool, and there is interest in coordination of these two platforms for invasive species information sharing for ma… [Source](https://pubs.usgs.gov/of/2020/1057/ofr20201057.pdf)
- [DOC001, pp. 27-29] **Missouri State Wildlife Action Plan** — and conservation partners will con- tinue to provide services statewide and constantly continue to explore valuable opportunities to con - serve Missouri’s natural communities and the spe- cies they support. The final selection criteria and COA maps for each habitat system are provided in the habita… [Source](https://www.mdc.mo.gov/sites/default/files/2020-04/SWAP_0.pdf)
- [DOC001, pp. 17-20] **Missouri State Wildlife Action Plan** — to promote conservation action with partners. The CWCS was designed to be adaptive, and this is reflected in the current State Wildlife Action Plan (Plan). The Plan is a revision of Missouri’s CWCS; the new title reflects a change in terminology for these na- tionwide plans at a national level. In t… [Source](https://www.mdc.mo.gov/sites/default/files/2020-04/SWAP_0.pdf)
- [DOC031, pp. 16-18] **DocumentCloud Public Search** — the 28 National Estuary Programs, have restored more than 10,000 acres of commercial shellfish beds despite significant population growth and development. The public-private efforts made by another National Estuary Program, the Sarasota Bay Project, have resulted in a 20 percent increase in seagrass… [Source](https://s3.documentcloud.org/documents/24223250/epa-2000-report-on-americas-water-resources.pdf)

### Answer

I do not have enough retrieved evidence in this corpus to answer that question.

### Manual review

- [ ] Retrieved chunks are relevant.
- [ ] Claims are supported by cited evidence.
- [ ] Document IDs and page numbers are correct.
- [ ] Unsupported claims are absent or the system abstained.
- Notes:

## 12. Which conservation claims are supported by documents from more than one agency?

Evaluation set: **Additional engineering question**

Status: `deterministic`

Retrieval mode: `structured_relations`

### Retrieved evidence

- [DOC014, pp. 18-20] **Habitat Matters** — A new culvert with headwall, inlet structure and grate for debris control. Riprap surrounding the h eadwall and an erosion control blanket and straw along the embankments help mitigate erosion. Bottom left: A revitalized drainage ditch. Ducks Unlimited Canada Funding constraints limited the scope of… [Source](https://publications.gc.ca/collections/collection_2025/eccc/CW71-8-2025-eng.pdf)
- [DOC001, pp. 149-153] **Missouri State Wildlife Action Plan** — achieve stream-floodplain-watershed conservation and restoration in Missouri by establishing an interdis- ciplinary statewide task force with participation from agencies and partners directly involved with stream-floodplain-watershed management. ✦ Improve management of wetland complexes to benefit w… [Source](https://www.mdc.mo.gov/sites/default/files/2020-04/SWAP_0.pdf)

### Answer

These exact extracted conservation relationships are independently supported by documents from different source agencies:

- **Mallard uses wetland habitat** — Environment and Climate Change Canada states: The wetlands will support species such as Mallard, Common Merganser and Barrow’s Goldeneye; Missouri Department of Conservation states: These improvements have resulted in wetland systems that provide habitat to species such as migrating soras, yellow rails, mallards, as well as digger crayfish and small-mouthed salamanders. [DOC014, pp. 18-20], [DOC001, pp. 149-153]

### Manual review

- [ ] Retrieved chunks are relevant.
- [ ] Claims are supported by cited evidence.
- [ ] Document IDs and page numbers are correct.
- [ ] Unsupported claims are absent or the system abstained.
- Notes:

## 13. Which retrieved evidence lacks a PDF page number and therefore needs URL-only citation?

Evaluation set: **Additional engineering question**

Status: `deterministic`

Retrieval mode: `page_audit`

### Retrieved evidence

- [DOC016] **MDC Annual Review FY2024** — Annual Review: Fiscal Year July 1, 2023 - June 30, 2024 By MDC | January 1, 2025 From Missouri Conservationist: January 2025 Stay In Touch Stay in Touch with MDC news, newsletters, events, and manage your subscription Link Sign Up View the Digital Magazine Download Issue 5.80 MB More Issues Media Im… [Source](https://mdc.mo.gov/magazines/missouri-conservationist/2025-01/annual-review-fiscal-year-july-1-2023-june-30-2024)
- [DOC016] **MDC Annual Review FY2024** — infrastructure projects were completed in Bonne Terre and Cape Girardeau. Aquatic Organism Passage Guided by the Southeast Aquatic Resource Partnership, MDC co-led, with The Nature Conservancy and the U.S. Fish and Wildlife Service, the formation of a statewide Missouri Stream Connectivity Partnersh… [Source](https://mdc.mo.gov/magazines/missouri-conservationist/2025-01/annual-review-fiscal-year-july-1-2023-june-30-2024)
- [DOC016] **MDC Annual Review FY2024** — grant project has provided an excellent opportunity to maintain and enhance fish habitat for two of the Midwest’s most popular sport fisheries. The work that has been accomplished on these projects has served as a national example of sustaining and improving reservoir sport fish populations through … [Source](https://mdc.mo.gov/magazines/missouri-conservationist/2025-01/annual-review-fiscal-year-july-1-2023-june-30-2024)
- [DOC016] **MDC Annual Review FY2024** — Nursery Celebrates 90 Years The George O. White State Forest Nursery has placed millions of trees on the state’s landscape since it began in 1934, and it celebrated its 90th anniversary on April 6, 2024, with a public open house. Staff conducted tours that provided insight into the science and techn… [Source](https://mdc.mo.gov/magazines/missouri-conservationist/2025-01/annual-review-fiscal-year-july-1-2023-june-30-2024)
- [DOC016] **MDC Annual Review FY2024** — and Tribal Forestry. Wildfire Going into FY24, Missouri was experiencing effects of drought conditions, which continued through May. Missouri received significant rainfall in June, relieving most of the drought conditions. Before rainfall arrived, MDC staff and partnering fire departments experience… [Source](https://mdc.mo.gov/magazines/missouri-conservationist/2025-01/annual-review-fiscal-year-july-1-2023-june-30-2024)
- [DOC016] **MDC Annual Review FY2024** — Assessment and Monitoring Strategic Initiative, which focuses resources on developing tools to assess and monitor the effectiveness of conservation actions within priority geographies. This work is being accomplished by developing achievable and desired future conditions using the Missouri River Hil… [Source](https://mdc.mo.gov/magazines/missouri-conservationist/2025-01/annual-review-fiscal-year-july-1-2023-june-30-2024)

### Answer

These retrieved evidence chunks have no stored PDF page number and therefore use document-only citations:

- `DOC016-C0001` from **MDC Annual Review FY2024** — [DOC016]
- `DOC016-C0002` from **MDC Annual Review FY2024** — [DOC016]
- `DOC016-C0003` from **MDC Annual Review FY2024** — [DOC016]
- `DOC016-C0004` from **MDC Annual Review FY2024** — [DOC016]
- `DOC016-C0005` from **MDC Annual Review FY2024** — [DOC016]
- `DOC016-C0006` from **MDC Annual Review FY2024** — [DOC016]

### Manual review

- [ ] Retrieved chunks are relevant.
- [ ] Claims are supported by cited evidence.
- [ ] Document IDs and page numbers are correct.
- [ ] Unsupported claims are absent or the system abstained.
- Notes:

## 14. What exact private MDC personnel records are contained in this public corpus?

Evaluation set: **Additional engineering question**

Status: `sufficiency_abstention`

Retrieval mode: `semantic`

### Retrieved evidence

- [DOC018] **MDC Annual Review FY2021** — Water, Urban League of Metro St. Louis, St. Louis County Police Department, and many others to participate in the “Clean Up, Build Up” project to help clean up the trash, debris, and overgrowth of invasive species in the underserved community of Castle Point in North St. Louis County. Several 40-yar… [Source](https://mdc.mo.gov/magazines/missouri-conservationist/2023-01/annual-review)
- [DOC018] **MDC Annual Review FY2021** — was taken to improve MDC’s competitiveness in an aggressive hiring market and to expand on total rewards for existing staff resulting in improved retention. Talent acquisition in collaboration with staff statewide filled a record number of personnel transactions in FY22. During this unprecedented ti… [Source](https://mdc.mo.gov/magazines/missouri-conservationist/2023-01/annual-review)
- [DOC020, pp. 65-69] **MDC Conservation Resources** — workplace. 63 HB Section(s): 6.625 PROGRAM DESCRIPTION Department of Conservation Program Name: Staff Development & Benefits Program is found in the following core budget(s): Staff Development & Benefits Employee Development 2a. Provide an activity measure(s) for the program. The Department promotes… [Source](https://mdc.mo.gov/sites/default/files/2022-06/FY23IEPbook.pdf)
- [DOC017] **MDC Annual Review FY2023** — the state of wetland conservation in Missouri. A Missouri Grasslands Summit is being planned for April 2024 with the same objective as the wetlands summit. Missouri Comprehensive Conservation Strategy During this past year, 19 regional Comprehensive Conservation Strategy (CCS) trainings were provide… [Source](https://mdc.mo.gov/magazines/missouri-conservationist/2024-01/annual-review-fiscal-year-2023)
- [DOC017] **MDC Annual Review FY2023** — will incorporate new technologies that will improve fish production and repair or replace sections of the hatchery that either are no longer functioning or functioning poorly due to age. This project will also improve staff safety during all seasons and weather events. Completion of this project wil… [Source](https://mdc.mo.gov/magazines/missouri-conservationist/2024-01/annual-review-fiscal-year-2023)
- [DOC016] **MDC Annual Review FY2024** — grant project has provided an excellent opportunity to maintain and enhance fish habitat for two of the Midwest’s most popular sport fisheries. The work that has been accomplished on these projects has served as a national example of sustaining and improving reservoir sport fish populations through … [Source](https://mdc.mo.gov/magazines/missouri-conservationist/2025-01/annual-review-fiscal-year-july-1-2023-june-30-2024)

### Answer

I do not have enough retrieved evidence in this corpus to answer that question.

### Manual review

- [ ] Retrieved chunks are relevant.
- [ ] Claims are supported by cited evidence.
- [ ] Document IDs and page numbers are correct.
- [ ] Unsupported claims are absent or the system abstained.
- Notes:

## 15. What evidence does this corpus provide about Amazon rainforest deforestation?

Evaluation set: **Additional engineering question**

Status: `structured_generated_narrowed`

Retrieval mode: `semantic`

### Retrieved evidence

- [DOC032, pp. 19-20] **DocumentCloud Environment Project Search** — principles and indicators such as the health of the land, caring for the country and reciprocal responsibility. As lifestyles, values and external pressures change with globalization, however, unsustainable practices are becoming increasingly common in certain regions 9. The central figure shows the… [Source](https://s3.documentcloud.org/documents/5990576/Summary-for-Policymakers-IPBES-Global-Assessment.pdf)
- [DOC032, pp. 17-18] **DocumentCloud Environment Project Search** — sources is already a major driver of negative environmental change. Ocean mining, while relatively small, has expanded since 1981 to ~ 6,500 offshore oil and gas installation worldwide in 53 countries (60% in the Gulf of Mexico by 2003) and likely will expand into the Arctic and Antarctic regions as… [Source](https://s3.documentcloud.org/documents/5990576/Summary-for-Policymakers-IPBES-Global-Assessment.pdf)
- [DOC029] **NOAA Habitat Conservation** — property values. NOAA practices habitat protection nationwide. Priority areas include rivers with sea-going fish , wetlands and estuaries, coral reefs, and large-scale bays and watersheds. We also explore and protect coral habitat in the deep sea, which is the least explored place on Earth. Our Key … [Source](https://www.fisheries.noaa.gov/topic/habitat-conservation)
- [DOC034, pp. 41-43] **DocumentCloud Conservation Search** — Environment are Inseparable ■ Canada's Goal is to Ensure that Citizens Today and Tomorrow Have the Clean Air, Water and Land Essential to Sustaining Human Health and the Environment. ■ Introduction Human health, the environment and the economy are inextricably linked. We humans arrive on Earth as in… [Source](https://s3.documentcloud.org/documents/6563087/Canada-s-Green-Plan-1990.pdf)
- [DOC013, pp. 231-233] **State Wildlife Action Plans Report with State Summaries** — alteration • Organic pollutants • Provide incentives to private landowners to restore and maintain shoreline and stream habitats. • Protect vegetated stream buffers to limit sedimentation. • Work with government agencies and industries on strategies to reduce contaminant discharges. Grassland Owners… [Source](https://www.fishwildlife.org/application/files/6415/1856/1631/StateWildlifeActionPlansReportwithStateSummaries.pdf)
- [DOC014, pp. 4-7] **Habitat Matters** — legal agreements with landowners (10-year minimum). 248.3 million acres of habitat influenced (100.5 million hectares) Involves direct actions that protect or enhance habitat without legal or bind- ing agreements. These actions result in land-use change. 4.3 million acres of habitat enhanced (1.7 mi… [Source](https://publications.gc.ca/collections/collection_2025/eccc/CW71-8-2025-eng.pdf)

### Answer

The retrieved evidence supports:

- (h) buffers for deforestation in recognized indigenous territories (Amazon basin, Brazil) {2.2.4.7}. [DOC032, pp. 19-20]

### Manual review

- [ ] Retrieved chunks are relevant.
- [ ] Claims are supported by cited evidence.
- [ ] Document IDs and page numbers are correct.
- [ ] Unsupported claims are absent or the system abstained.
- Notes:
