import type { Metadata } from "next";
import type { ReactNode } from "react";

import { Nav } from "@/components/nav";
import "./globals.css";

export const metadata: Metadata = {
  title: {
    default: "FTV",
    template: "%s · FTV",
  },
  description:
    "Dashboard shell for six-month transfer-value predictions across the Big 5 leagues and the Champions League.",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <div className="shell">
          <header className="topbar">
            <a className="mark" href="/">
              <strong>FTV</strong>
              <span>Δ six months</span>
            </a>
            <Nav />
          </header>
          <main>{children}</main>
          <footer className="footer">
            Mocked predictions for the Big 5 leagues and the Champions League.
            Valuation pages are not a data source. Paid football APIs are not
            configured. ClubElo is the free ratings stub.
          </footer>
        </div>
      </body>
    </html>
  );
}
