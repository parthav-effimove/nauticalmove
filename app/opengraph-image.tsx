import { ImageResponse } from "next/og";

export const runtime = "edge";
export const alt =
  "nauticalmove — maritime intelligence for better commercial decisions";
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

export default function OpenGraphImage() {
  return new ImageResponse(
    (
      <div
        style={{
          position: "relative",
          display: "flex",
          flexDirection: "column",
          width: "100%",
          height: "100%",
          overflow: "hidden",
          padding: "64px 88px",
          color: "#ffffff",
          background: "linear-gradient(120deg, #07131e 0%, #102a35 65%, #15333e 100%)",
          fontFamily: "Arial, Helvetica, sans-serif",
        }}
      >
        <div
          style={{
            position: "absolute",
            top: -180,
            right: -30,
            width: 650,
            height: 850,
            border: "1px solid rgba(84, 213, 210, 0.14)",
            transform: "rotate(28deg)",
          }}
        />
        <div
          style={{
            position: "absolute",
            top: -180,
            right: 115,
            width: 650,
            height: 850,
            border: "1px solid rgba(84, 213, 210, 0.1)",
            transform: "rotate(28deg)",
          }}
        />
        <div
          style={{
            position: "absolute",
            top: 176,
            right: 246,
            width: 11,
            height: 11,
            borderRadius: "50%",
            background: "#54d5d2",
          }}
        />
        <div
          style={{
            position: "absolute",
            top: 358,
            right: 137,
            width: 11,
            height: 11,
            borderRadius: "50%",
            background: "#54d5d2",
          }}
        />

        <div style={{ display: "flex", alignItems: "center", gap: 18 }}>
          <div
            style={{
              display: "flex",
              width: 62,
              height: 62,
              alignItems: "center",
              justifyContent: "center",
              border: "1px solid rgba(84, 213, 210, 0.65)",
              borderRadius: 15,
              background: "rgba(84, 213, 210, 0.08)",
            }}
          >
            <svg width="42" height="48" viewBox="0 0 100 110" fill="none">
              <circle cx="50" cy="55" r="39" stroke="#54d5d2" strokeWidth="3" />
              <path d="M61 28 48 53 36 82 59 64 72 36 61 28Z" fill="#54d5d2" />
              <path d="m61 28-13 25-12 2 25-27Z" fill="#ffffff" />
              <circle cx="49" cy="55" r="3" fill="#ffffff" />
            </svg>
          </div>
          <div
            style={{
              display: "flex",
              fontSize: 38,
              fontWeight: 700,
              letterSpacing: -1.8,
            }}
          >
            nauticalmove
          </div>
        </div>

        <div style={{ display: "flex", flexDirection: "column", marginTop: 66 }}>
          <div
            style={{
              display: "flex",
              fontSize: 57,
              fontWeight: 600,
              lineHeight: 1.12,
              letterSpacing: -2.6,
            }}
          >
            Maritime intelligence for
          </div>
          <div
            style={{
              display: "flex",
              color: "#54d5d2",
              fontSize: 57,
              fontWeight: 600,
              lineHeight: 1.12,
              letterSpacing: -2.6,
            }}
          >
            better commercial decisions.
          </div>
          <div
            style={{
              display: "flex",
              marginTop: 22,
              color: "#c5d2d7",
              fontSize: 21,
              letterSpacing: 0.2,
            }}
          >
            Voyage estimation · Cargo flows · Fixture insights
          </div>
        </div>

        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            marginTop: "auto",
            paddingTop: 20,
            borderTop: "1px solid rgba(255, 255, 255, 0.18)",
            color: "#91a7b0",
            fontSize: 13,
            fontWeight: 600,
            letterSpacing: 1.8,
          }}
        >
          <div style={{ display: "flex" }}>DRY BULK + TANKERS</div>
          <div style={{ display: "flex" }}>NAUTICALMOVE.COM</div>
        </div>
      </div>
    ),
    { ...size },
  );
}
