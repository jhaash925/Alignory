import { Link, useLocation } from "react-router-dom";

const navItems = [
  { label: "Home", path: "/" },
  { label: "Job Match", path: "/job-match" },
  { label: "General Review", path: "/general-review" },
  { label: "Resume Builder", path: "/resume-builder" }
];

function SiteHeader() {
  const location = useLocation();

  return (
    <header className="sticky top-0 z-30 px-4 pt-4 md:px-8">
      <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 rounded-[24px] border border-white/70 bg-[rgba(255,255,255,0.76)] px-4 py-3 shadow-[0_10px_30px_rgba(15,23,42,0.06)] backdrop-blur">
        <Link to="/" className="flex items-center gap-3">
          <div className="relative flex h-10 w-10 items-center justify-center rounded-[18px] bg-slate-900 shadow-[0_8px_18px_rgba(15,23,42,0.12)]">
            <div className="relative h-5.5 w-4.5 rounded-[6px] bg-white/95">
              <div className="absolute left-[3px] top-[4px] h-[2px] w-2.5 rounded-full bg-slate-900/80" />
              <div className="absolute left-[3px] top-[8px] h-[2px] w-3 rounded-full bg-slate-900/55" />
              <div className="absolute left-[3px] top-[12px] h-[2px] w-2 rounded-full bg-slate-900/55" />
              <div className="absolute -right-1 -top-1 flex h-3.5 w-3.5 items-center justify-center rounded-full bg-teal-400 ring-2 ring-slate-900">
                <div className="h-1.5 w-1.5 rounded-full bg-slate-900" />
              </div>
            </div>
          </div>

          <div>
            <div className="text-2xl font-bold leading-none text-slate-900">
              Alignory
            </div>
            <div className="mt-1 text-[10px] font-semibold uppercase tracking-[0.2em] text-slate-500">
              Resume Intelligence
            </div>
          </div>
        </Link>

        <nav className="hidden items-center gap-1.5 lg:flex">
          {navItems.map((item) => {
            const isActive = location.pathname === item.path;

            return (
              <Link
                key={item.path}
                to={item.path}
                className={`rounded-full px-3.5 py-2 text-sm font-semibold transition ${
                  isActive
                    ? "bg-slate-900 text-white"
                    : "text-slate-600 hover:bg-white/85 hover:text-slate-900"
                }`}
              >
                {item.label}
              </Link>
            );
          })}
        </nav>
      </div>
    </header>
  );
}

export default SiteHeader;
