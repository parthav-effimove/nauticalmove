"use client";

import { useState } from "react";
import Link from "next/link";
import { ArrowRight, Menu, X } from "lucide-react";

const navigation = [["All Tools", "/solutions"], ["Markets", "/markets"], ["Insights", "/intelligence"], ["Contact Us", "/company"]];

export function Logo() {
  return <Link className="logo" href="/" aria-label="NauticalMove"><img className="logo-image" src="/nauticalmove-logo.svg" alt="nauticalmove" /></Link>;
}

export function SiteHeader() {
  const [menuOpen, setMenuOpen] = useState(false);
  return <header className="site-header"><div className="nav-wrap"><Logo /><nav id="site-navigation" className={menuOpen ? "nav-links is-open" : "nav-links"} aria-label="Main navigation">{navigation.map(([label, href]) => <Link key={href} href={href} onClick={() => setMenuOpen(false)}>{label}</Link>)}</nav><Link className="nav-cta" href="/company#enquiry">Access <ArrowRight size={15} /></Link><button className="menu-button" aria-label={menuOpen ? "Close navigation" : "Open navigation"} aria-expanded={menuOpen} aria-controls="site-navigation" onClick={() => setMenuOpen(!menuOpen)}>{menuOpen ? <X size={22} /> : <Menu size={22} />}</button></div></header>;
}

export function SiteFooter() {
  return <footer className="site-footer"><div className="page-width footer-top"><div><Logo /><p>Data &amp; Analytics</p></div><div className="footer-links">{navigation.map(([label, href]) => <Link key={href} href={href}>{label}</Link>)}<Link href="/company#enquiry">Access</Link></div></div><div className="page-width footer-bottom"><span>© 2026 NauticalMove</span><span>Data &amp; APIs</span></div></footer>;
}
