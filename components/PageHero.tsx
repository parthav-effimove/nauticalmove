import Link from "next/link";
import { ArrowRight } from "lucide-react";

export function PageHero({ eyebrow, title, description, action = "Access", href = "/company#enquiry" }: { eyebrow: string; title: React.ReactNode; description: string; action?: string; href?: string }) {
  return <section className="page-hero"><div className="page-hero-grid" aria-hidden="true" /><div className="page-width page-hero-content"><p className="kicker"><span className="status-dot" /> {eyebrow}</p><h1>{title}</h1><p>{description}</p><Link className="button" href={href}>{action} <ArrowRight size={16} /></Link></div></section>;
}
