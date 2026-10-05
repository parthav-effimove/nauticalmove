import Link from "next/link";
import { ArrowRight, BarChart3, Compass, Network, Ship } from "lucide-react";
import { SiteFooter, SiteHeader } from "../components/SiteChrome";

<<<<<<< HEAD
import { FormEvent, useState } from "react";
import {
  ArrowDown,
  ArrowRight,
  BarChart3,
  ChevronDown,
  Compass,
  Container,
  Globe2,
  Menu,
  Network,
  Ship,
  Sparkles,
  X,
} from "lucide-react";

const capabilityCards = [
  {
    number: "01",
    eyebrow: "Voyage Estimation",
    title: "Understand the economics of every voyage.",
    description:
      "Evaluate voyage scenarios using vessel, cargo, routing, fuel, port and commercial parameters to understand voyage economics.",
    icon: Compass,
    tags: ["Voyage economics", "Distance & routing", "Fuel consumption", "Bunker costs", "Port costs", "Voyage P&L"],
  },
  {
    number: "02",
    eyebrow: "Cargo Flows",
    title: "Understand where cargo is moving.",
    description:
      "Analyze global cargo movements, trade routes and port-to-port flows to understand the relationship between commodities, vessels and markets.",
    icon: Network,
    tags: ["Global trade flows", "Commodity movements", "Origin & destination", "Port-to-port flows", "Vessel movements", "Historical flows"],
  },
  {
    number: "03",
    eyebrow: "Fixtures",
    title: "Turn fixture activity into market intelligence.",
    description:
      "Understand fixtures through structured information covering vessels, cargoes, charterers, owners, routes, rates and laycans.",
    icon: BarChart3,
    tags: ["Fixtures", "Vessel", "Owner", "Charterer", "Cargo", "Laycan", "Rate"],
  },
];

const audiences = [
  ["Ship Owners", "See the commercial picture around your fleet and the voyages it can take."],
  ["Charterers", "Connect cargo requirements, vessel options and market context."],
  ["Ship Brokers", "Bring structured market information into every conversation."],
  ["Operators", "Frame operational choices with clearer voyage economics."],
  ["Traders", "Follow cargo flows, routes and the commercial signals behind them."],
  ["Maritime Analysts", "Work from a connected view of vessels, cargoes and fixtures."],
];

function AnchorButton({ children, href, secondary = false }: { children: React.ReactNode; href: string; secondary?: boolean }) {
  return <a className={secondary ? "button button-secondary" : "button"} href={href}>{children}<ArrowRight size={16} /></a>;
}

function Logo() {
  return <a className="logo" href="#home" aria-label="nauticalmove home"><img className="logo-image" src="/nauticalmove-logo.svg" alt="nauticalmove" /></a>;
}

export default function Home() {
  const [menuOpen, setMenuOpen] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  function submitForm(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitted(true);
  }

  return (
    <main>
      <header className="site-header">
        <div className="nav-wrap">
          <Logo />
          <nav id="primary-navigation" className={menuOpen ? "nav-links is-open" : "nav-links"} aria-label="Primary navigation">
            {["Solutions", "Markets", "About", "Contact"].map((item) => (
              <a key={item} href={`#${item.toLowerCase()}`} onClick={() => setMenuOpen(false)}>{item}</a>
            ))}
          </nav>
          <a className="nav-cta" href="#contact">Contact us <ArrowRight size={15} /></a>
          <button type="button" className="menu-button" aria-label={menuOpen ? "Close menu" : "Open menu"} aria-expanded={menuOpen} aria-controls="primary-navigation" onClick={() => setMenuOpen(!menuOpen)}>{menuOpen ? <X size={22} /> : <Menu size={22} />}</button>
        </div>
      </header>

      <section className="hero" id="home">
        <div className="hero-art" aria-hidden="true"><div className="hero-art-overlay" /><div className="hero-point point-one" /><div className="hero-point point-two" /><div className="hero-point point-three" /></div>
        <div className="hero-content page-width">
          <div className="kicker"><span className="status-dot" /> Maritime commercial intelligence</div>
          <h1>Maritime intelligence for <em>better</em> commercial decisions.</h1>
          <p className="hero-copy">nauticalmove brings together voyage estimation, cargo-flow intelligence and fixture insights across global dry bulk and tanker markets.</p>
          <div className="hero-actions"><AnchorButton href="#solutions">Explore our solutions</AnchorButton><AnchorButton href="#contact" secondary>Contact us</AnchorButton></div>
          <div className="hero-meta"><span>GLOBAL COVERAGE</span><span className="meta-rule" /><span>DRY BULK + TANKERS</span></div>
        </div>
        <a className="scroll-cue" href="#solutions" aria-label="Scroll to solutions"><ArrowDown size={17} /><span>Scroll to explore</span></a>
      </section>

      <section className="intro-section page-width" id="solutions">
        <div className="section-label">01 / What we connect</div>
        <div className="intro-grid"><h2>See the market<br /><span>in motion.</span></h2><p>Maritime commerce is a network of moving parts. nauticalmove makes the connection between them clearer, so commercial teams can move from scattered signals to a more complete point of view.</p></div>
      </section>

      <section className="capabilities-section page-width" aria-label="Core capabilities">
        {capabilityCards.map((card) => { const Icon = card.icon; return <article className="capability-card" key={card.number}><div className="card-topline"><span className="card-number">{card.number}</span><Icon size={22} strokeWidth={1.5} /></div><p className="eyebrow">{card.eyebrow}</p><h3>{card.title}</h3><p className="muted">{card.description}</p><div className="tag-list">{card.tags.map((tag) => <span key={tag}>{tag}</span>)}</div><a className="card-link" href="#contact">Learn more <ArrowRight size={15} /></a></article>; })}
      </section>

      <section className="market-section" id="markets"><div className="page-width"><div className="section-label light">02 / Market coverage</div><div className="market-heading"><h2>Across dry bulk<br />&amp; <span>tanker</span> markets.</h2><p>Built around the commercial realities of two of the world&apos;s most important maritime markets.</p></div><div className="market-grid"><MarketCard type="Dry Bulk" code="DB" segments={["Capesize", "Panamax", "Ultramax", "Supramax", "Handysize"]} cargo={["Iron Ore", "Coal", "Grain", "Bauxite", "Fertilizers"]} /><MarketCard type="Tankers" code="TK" segments={["VLCC", "Suezmax", "Aframax", "LR2", "LR1", "MR", "Handy"]} cargo={["Crude Oil", "Refined Products", "Clean Petroleum Products", "Chemicals"]} /></div></div></section>

      <section className="connect-section page-width"><div className="section-label">03 / The nauticalmove view</div><div className="connect-heading"><h2>One connected view<br /><span>of the market.</span></h2><p>When vessels, cargoes, routes and fixtures are seen together, commercial intelligence becomes more useful.</p></div><div className="flow-line">{["Vessels", "Cargo", "Routes", "Fixtures", "Voyage economics", "Market intelligence"].map((item, index) => <div className="flow-item" key={item}><span className={index === 5 ? "flow-icon final" : "flow-icon"}>{index === 5 ? <Sparkles size={17} /> : index === 0 ? <Ship size={17} /> : index === 1 ? <Container size={17} /> : index === 2 ? <Globe2 size={17} /> : <BarChart3 size={17} />}</span><strong>{item}</strong>{index < 5 && <ArrowRight className="flow-arrow" size={17} />}</div>)}</div></section>

      <section className="voyage-section"><div className="page-width voyage-grid"><div><div className="section-label light">04 / Voyage intelligence</div><h2>From vessel data<br />to <span>voyage economics.</span></h2><p>Put the commercial shape of a voyage into focus by following the chain of decisions that defines it.</p></div><div className="voyage-stack">{["Vessel", "Cargo", "Load port", "Discharge port", "Distance", "Fuel & port costs", "Freight / revenue", "Voyage economics"].map((item, index) => <div className={index === 7 ? "voyage-step final" : "voyage-step"} key={item}><span>0{index + 1}</span><strong>{item}</strong>{index < 7 && <ArrowDown size={15} />}</div>)}</div></div></section>

      <section className="why-section page-width"><div className="section-label">05 / Why nauticalmove</div><div className="why-grid"><h2>Commercial clarity,<br /><span>connected.</span></h2><div className="why-cards">{[["Data driven", "Turn maritime data into actionable commercial intelligence."], ["Market focused", "Built around the realities of dry bulk and tanker markets."], ["Connected", "Connect vessels, cargoes, routes and fixtures."], ["Commercial", "Focus on information that supports real-world maritime decisions."]].map(([title, text], i) => <div className="why-card" key={title}><span>0{i + 1}</span><h3>{title}</h3><p>{text}</p></div>)}</div></div></section>

      <section className="audience-section" id="about"><div className="page-width"><div className="section-label light">06 / Built for the people moving markets</div><div className="audience-heading"><h2>Built for maritime<br /><span>commercial teams.</span></h2><p>nauticalmove is a maritime technology and intelligence company focused on making commercial data more accessible, connected and actionable.</p></div><div className="audience-grid">{audiences.map(([title, text], i) => <div className="audience-item" key={title}><span className="audience-index">0{i + 1}</span><div><h3>{title}</h3><p>{text}</p></div><ArrowRight size={18} /></div>)}</div></div></section>

      <section className="about-strip"><div className="page-width about-strip-inner"><div><div className="section-label light">07 / Our focus</div><h2>Understanding maritime<br /><span>commerce through data.</span></h2></div><div className="about-copy"><p><strong>Mission</strong> To make maritime commercial intelligence more accessible, connected and actionable.</p><p><strong>Vision</strong> To build a connected intelligence layer for global maritime commerce.</p></div></div></section>

      <section className="contact-section page-width" id="contact"><div className="contact-grid"><div><div className="section-label">08 / Start a conversation</div><h2>Let&apos;s talk maritime <span>intelligence.</span></h2><p>Interested in learning more about nauticalmove and our maritime intelligence capabilities? Get in touch with our team.</p><div className="contact-note"><span className="status-dot" /> We&apos;ll get back to you with the right starting point.</div></div><div className="tally-frame contact-tally-frame"><iframe src="https://tally.so/r/WOx6RR?transparentBackground=1&hideTitle=1" title="nauticalmove enquiry form" loading="lazy" /></div></div></section>

      <footer className="site-footer"><div className="page-width footer-top"><div><Logo /><p>Maritime commercial intelligence.</p></div><div className="footer-links">{["Solutions", "Markets", "About", "Contact"].map((item) => <a key={item} href={`#${item.toLowerCase()}`}>{item}</a>)}</div></div><div className="page-width footer-bottom"><span>© 2026 nauticalmove. All rights reserved.</span><span>Global maritime intelligence</span></div></footer>
    </main>
  );
}

function MarketCard({ type, code, segments, cargo }: { type: string; code: string; segments: string[]; cargo: string[] }) {
  return <article className="market-card"><div className="market-card-head"><div><span className="eyebrow">Market</span><h3>{type}</h3></div><span className="market-code">{code}</span></div><div className="market-card-body"><div><span className="mini-label">Vessel segments</span><div className="pill-list">{segments.map((segment) => <span key={segment}>{segment}</span>)}</div></div><div><span className="mini-label">Cargo examples</span><div className="pill-list">{cargo.map((item) => <span key={item}>{item}</span>)}</div></div></div><div className="market-card-foot"><span>Commercial coverage</span><ArrowRight size={16} /></div></article>;
=======
const tools = [["Voyage Estimator", "Calculate voyage returns and break-even freight rates with integrated data.", Compass, "/solutions#estimator"], ["Trade Flows", "Explore trade patterns by commodity and port.", Network, "/solutions#trade-flows"], ["Fixtures", "Search commercial data and explore fixture history.", BarChart3, "/solutions#fixtures"]] as const;

export default function Home() {
  return <main><SiteHeader /><section className="hero home-hero"><div className="hero-art" aria-hidden="true"><div className="hero-art-overlay" /><div className="hero-point point-one" /><div className="hero-point point-two" /></div><div className="hero-content page-width"><div className="kicker"><span className="status-dot" /> Live AIS-derived data</div><h1>NauticalMove <em>chartering</em> tools.</h1><p className="hero-copy">Compare voyages, explore cargo flows and search fixtures with shipping data.</p><div className="hero-actions"><Link className="button" href="/solutions">All Tools <ArrowRight size={16} /></Link><Link className="button button-secondary" href="/markets">Market data <ArrowRight size={16} /></Link></div><div className="hero-meta"><span>LIVE AIS DATA</span><span className="meta-rule" /><span>DRY BULK + TANKER</span></div></div></section>
    <section className="home-intro page-width"><div className="section-label">Data &amp; Analytics</div><div className="split-intro"><h2>Vessel and <span>commodity flows.</span></h2><p>Explore vessel movements and commodity demand for informed chartering decisions.</p></div></section>
    <section className="solution-preview page-width">{tools.map(([title, description, Icon, href], index) => <article className="solution-preview-card" key={title}><div><span className="card-number">0{index + 1}</span><Icon size={25} strokeWidth={1.4} /></div><h3>{title}</h3><p>{description}</p><Link href={href}>Read more <ArrowRight size={15} /></Link></article>)}</section>
    <section className="market-band"><div className="page-width market-band-grid"><div><div className="section-label light">By Market</div><h2>Dry Bulk and <span>Tanker.</span></h2></div><div><p>Explore supply and demand across Dry Bulk and Tanker markets.</p><Link className="text-link light-link" href="/markets">Read more <ArrowRight size={15} /></Link></div></div></section>
    <section className="operating-model page-width"><div className="section-label">Data &amp; APIs</div><div className="operating-head"><h2>Vessels, cargoes, routes and <span>market data.</span></h2><p>Access ports, positions, cargoes, bunker prices, fixtures, vessels and indices via APIs.</p></div><div className="operating-flow">{["Vessels", "Cargoes", "Ports", "Fixtures", "Bunker prices", "Indices"].map((item, i) => <div key={item}><span>{i === 0 ? <Ship size={18} /> : `0${i + 1}`}</span><strong>{item}</strong></div>)}</div></section>
    <section className="home-cta"><div className="page-width"><div><div className="section-label light">Contact Us</div><h2>Access <span>market analytics.</span></h2></div><Link className="button" href="/company#enquiry">Contact Us <ArrowRight size={16} /></Link></div></section><SiteFooter /></main>;
>>>>>>> 9b329b8 (update content)
}
