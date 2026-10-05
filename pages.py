# pages.py  -  Panel v9.8
# شامل: LOGIN_HTML, DASHBOARD_HTML, get_public_page_html()


LOGIN_HTML = r"""<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Sign in · Panel</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#121417;--card:#1a1d22;--border:#2a2f36;--text:#e5e8ec;--mid:#a5adb9;--dim:#707988;--accent:#6f9cf0;--accent-s:#3f73d9;--input:#14171b}
html,body{height:100%}
body{font-family:'IBM Plex Sans',system-ui,sans-serif;background:var(--bg);color:var(--text);display:flex;align-items:center;justify-content:center;padding:20px;font-size:14px;line-height:1.5;-webkit-font-smoothing:antialiased}
.wrap{width:100%;max-width:380px}
.brand{display:flex;align-items:baseline;gap:8px;margin-bottom:18px;padding:0 2px}
.brand-name{font-size:18px;font-weight:600}
.brand-sub{font-size:12px;color:var(--dim)}
.card{background:var(--card);border:1px solid var(--border);border-radius:6px;padding:28px 28px 26px}
h1{font-size:18px;font-weight:600;margin-bottom:4px}
.sub{font-size:13px;color:var(--mid);margin-bottom:22px}
.field{margin-bottom:16px}
.field label{display:block;font-size:12.5px;font-weight:500;color:var(--mid);margin-bottom:6px}
.inp-wrap{position:relative}
input[type=password]{width:100%;padding:10px 40px 10px 12px;border-radius:4px;border:1px solid var(--border);background:var(--input);color:var(--text);font-family:inherit;font-size:14px;outline:none;transition:border-color .12s}
input[type=password]::placeholder{color:var(--dim)}
input[type=password]:focus{border-color:var(--accent);box-shadow:0 0 0 2px rgba(111,156,240,.18)}
.ic{position:absolute;right:12px;top:50%;transform:translateY(-50%);color:var(--dim);font-size:17px;pointer-events:none}
.err{display:none;background:rgba(217,96,90,.12);border:1px solid rgba(217,96,90,.35);border-radius:4px;padding:9px 12px;margin-bottom:14px;font-size:13px;color:#ef8c87;align-items:center;gap:8px}
.err.show{display:flex}
.btn{width:100%;padding:10px;border-radius:4px;border:1px solid transparent;cursor:pointer;background:var(--accent-s);color:#fff;font-family:inherit;font-size:14px;font-weight:600;display:flex;align-items:center;justify-content:center;gap:8px;transition:background .12s}
.btn:hover{background:#4a7fe6}
.btn:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.btn:disabled{opacity:.55;cursor:not-allowed}
@keyframes spin{to{transform:rotate(360deg)}}
</style>
</head>
<body>
<div class="wrap">
  <div class="brand"><span class="brand-name">Panel</span><span class="brand-sub">v9.8</span></div>
  <div class="card">
    <h1>Sign in</h1>
    <p class="sub">Enter your password to access the panel.</p>
    <div class="err" id="err"><i class="ti ti-alert-circle"></i><span id="err-text"></span></div>
    <form id="form">
      <div class="field">
        <label for="pw">Password</label>
        <div class="inp-wrap">
          <input type="password" id="pw" placeholder="Enter your password" autocomplete="current-password" autofocus required>
          <i class="ti ti-lock ic"></i>
        </div>
      </div>
      <button class="btn" type="submit" id="btn">Sign in</button>
    </form>
  </div>
</div>
<script>
document.getElementById('form').addEventListener('submit',async e=>{
  e.preventDefault();
  const btn=document.getElementById('btn'),err=document.getElementById('err'),et=document.getElementById('err-text');
  err.classList.remove('show');btn.disabled=true;
  btn.innerHTML='<i class="ti ti-loader-2" style="animation:spin 1s linear infinite"></i> Signing in...';
  try{
    const r=await fetch('/api/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({password:document.getElementById('pw').value})});
    if(!r.ok){const d=await r.json().catch(()=>({}));throw new Error(d.detail||'Error');}
    location.href='/panel';
  }catch(e){
    et.textContent=e.message;err.classList.add('show');
    btn.disabled=false;btn.textContent='Sign in';
  }
});
</script>
</body></html>"""


DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Panel</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#121417;--bg2:#171a1e;--bg3:#1e2227;--card:#1a1d22;--card-b:#2a2f36;--card-bh:#3b424c;--accent:#6f9cf0;--accent2:#9bb8f4;--accent-s:#3f73d9;--accent-d:rgba(111,156,240,0.10);--green:#3fa77a;--green-bg:rgba(63,167,122,0.12);--green-t:#6fcb9f;--red:#d9605a;--red-bg:rgba(217,96,90,0.12);--red-t:#ef8c87;--amber:#c99a3c;--amber-bg:rgba(201,154,60,0.12);--amber-t:#e2bd70;--purple:#8791a1;--purple-bg:rgba(135,145,161,0.14);--purple-t:#a3acb9;--t1:#e5e8ec;--t2:#a5adb9;--t3:#707988;--input:#14171b;--radius:6px;--shadow:none;--sidebar-w:240px;
}
[data-theme="light"]{
  --bg:#f2f3f5;--bg2:#e9ebee;--bg3:#e0e3e7;--card:#ffffff;--card-b:#d5d9df;--card-bh:#b9bfc8;--accent:#2f62c4;--accent2:#244e9f;--accent-s:#2f62c4;--accent-d:rgba(47,98,196,0.08);--green:#1f8a5e;--green-bg:rgba(31,138,94,0.10);--green-t:#176e4b;--red:#c0392f;--red-bg:rgba(192,57,47,0.09);--red-t:#9e2c24;--amber:#b07d1a;--amber-bg:rgba(176,125,26,0.10);--amber-t:#80590f;--purple:#5f6b7d;--purple-bg:rgba(95,107,125,0.10);--purple-t:#4a5565;--t1:#1b1f24;--t2:#454d59;--t3:#7a828e;--input:#ffffff;--shadow:none;
}
html,body{height:100%}
body{font-family:'IBM Plex Sans',sans-serif;background:var(--bg);color:var(--t1);min-height:100vh;display:flex;font-size:14px;transition:background .3s,color .3s}
::-webkit-scrollbar{width:5px;height:5px}
::-webkit-scrollbar-track{background:var(--bg)}
::-webkit-scrollbar-thumb{background:var(--bg3);border-radius:3px}
a{color:inherit;text-decoration:none}
.sidebar{width:var(--sidebar-w);min-height:100vh;background:var(--bg2);border-right:1px solid var(--card-b);display:flex;flex-direction:column;flex-shrink:0;position:fixed;left:0;top:0;bottom:0;z-index:200;transition:transform .25s cubic-bezier(.4,0,.2,1),background .3s,border-color .3s}
.logo{display:flex;align-items:center;gap:12px;padding:20px 16px 16px;border-bottom:1px solid var(--card-b)}
.logo-img{width:38px;height:38px;border-radius:50%;overflow:hidden;border:1px solid var(--card-b);box-shadow:0 0 14px rgba(135,145,161,.3),0 0 8px rgba(111,156,240,.25);flex-shrink:0}
.logo-img img{width:100%;height:100%;object-fit:cover}
.logo-name{font-size:13.5px;font-weight:700;color:var(--t1)}
.logo-sub{font-size:10px;color:var(--t3);margin-top:1px}
.sb-close{display:none;position:absolute;right:12px;top:20px;background:var(--accent-d);border:1px solid var(--card-b);color:var(--t2);width:30px;height:30px;border-radius:8px;font-size:16px;align-items:center;justify-content:center;cursor:pointer}
.nav-wrap{flex:1;overflow-y:auto;padding:6px 0 8px}
.nav-sec{padding:14px 14px 4px;font-size:9px;letter-spacing:.14em;text-transform:uppercase;color:var(--t3);font-weight:700}
.nav-it{display:flex;align-items:center;gap:9px;padding:9px 14px;color:var(--t3);font-size:12.5px;cursor:pointer;border-left:2px solid transparent;transition:all .15s;margin:1px 6px}
.nav-it i{font-size:16px;width:18px;text-align:center;flex-shrink:0}
.nav-it:hover{background:var(--accent-d);color:var(--t2)}
.nav-it.on{background:var(--accent-d);color:var(--t1);border-left-color:var(--accent);font-weight:600}
.nav-badge{margin-left:auto;background:rgba(111,156,240,0.15);color:var(--accent2);font-size:9px;padding:1px 6px;border-radius:20px;font-weight:700}
.sb-foot{padding:12px 14px;border-top:1px solid var(--card-b)}
.tg-btn{display:flex;align-items:center;justify-content:center;gap:8px;background:linear-gradient(135deg,#0098e6,#0077bb);color:#fff;border-radius:9px;padding:10px;font-size:12.5px;font-weight:600;font-family:inherit;border:none;cursor:pointer;width:100%;transition:.15s}
.tg-btn:hover{filter:brightness(1.1)}
.theme-btn{display:flex;align-items:center;justify-content:center;gap:7px;background:var(--accent-d);color:var(--t2);border-radius:9px;padding:8px;font-size:12px;font-weight:500;font-family:inherit;border:1px solid var(--card-b);cursor:pointer;width:100%;transition:.15s;margin-bottom:7px}
.theme-btn:hover{background:var(--card-b);color:var(--t1)}
.logout-btn{display:flex;align-items:center;justify-content:center;gap:7px;background:var(--red-bg);color:var(--red-t);border-radius:9px;padding:8px;font-size:12px;font-weight:500;font-family:inherit;border:1px solid rgba(239,68,68,0.2);cursor:pointer;width:100%;transition:.15s;margin-top:6px}
.logout-btn:hover{background:rgba(239,68,68,0.2)}
.mob-top{display:none;position:fixed;top:0;left:0;right:0;height:52px;background:var(--bg2);border-bottom:1px solid var(--card-b);z-index:150;align-items:center;justify-content:space-between;padding:0 14px;transition:background .3s}
.mob-top .ml{display:flex;align-items:center;gap:9px}
.mob-logo{width:28px;height:28px;border-radius:50%;overflow:hidden;box-shadow:0 0 8px rgba(135,145,161,.35)}
.mob-logo img{width:100%;height:100%;object-fit:cover}
.mob-title{color:var(--t1);font-size:13px;font-weight:700}
.mob-right{display:flex;gap:6px}
.menu-btn,.theme-mob{background:var(--accent-d);border:1px solid var(--card-b);color:var(--t2);width:34px;height:34px;border-radius:8px;font-size:17px;display:flex;align-items:center;justify-content:center;cursor:pointer;transition:.15s}
.overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.55);z-index:190;backdrop-filter:blur(3px)}
.overlay.show{display:block}
.main{margin-left:var(--sidebar-w);flex:1;padding:28px 28px 60px;min-width:0;transition:margin .25s}
.pg{display:none}
.pg.on{display:block;animation:fi .2s ease}
@keyframes fi{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
.topbar{display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:22px;flex-wrap:wrap;gap:12px}
.tb-title{font-size:18px;font-weight:700;color:var(--t1);display:flex;align-items:center;gap:8px;letter-spacing:-.02em}
.tb-title i{color:var(--accent);font-size:20px}
.tb-sub{font-size:11px;color:var(--t3);margin-top:4px}
.tb-right{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.badge{font-size:10px;padding:3px 10px;border-radius:20px;font-weight:700;display:inline-flex;align-items:center;gap:5px;white-space:nowrap}
.bg-green{background:var(--green-bg);color:var(--green-t)}
.bg-blue{background:var(--accent-d);color:var(--accent2)}
.bg-amber{background:var(--amber-bg);color:var(--amber-t)}
.bg-red{background:var(--red-bg);color:var(--red-t)}
.bg-purple{background:var(--purple-bg);color:#a3acb9}
.dot{width:6px;height:6px;border-radius:50%;flex-shrink:0;display:inline-block}
.dg{background:var(--green)}.dr{background:var(--red)}.da{background:var(--amber)}.db{background:var(--accent)}
.pulse{animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}
.metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:13px;margin-bottom:18px}
.metric{background:var(--card);border:1px solid var(--card-b);border-radius:var(--radius);padding:17px 17px 14px;transition:all .2s;position:relative;overflow:hidden;cursor:default}
.metric::after{content:'';position:absolute;top:0;left:0;width:3px;height:100%;background:var(--accent);opacity:0;transition:.2s}
.metric:hover{border-color:var(--card-bh);transform:translateY(-2px);box-shadow:var(--shadow)}
.metric:hover::after{opacity:1}
.metric.suc::after{background:var(--green)}
.metric.dan::after{background:var(--red)}
/* ══════ صفحه ترافیک - ریدیزاین ══════ */
.traf-hero{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:13px;margin-bottom:18px}
.traf-main-stat{background:linear-gradient(155deg,var(--bg3) 0%,var(--card) 60%);border:1px solid var(--card-b);border-radius:20px;padding:22px 24px;position:relative;overflow:hidden}
.traf-main-stat::before{content:'';position:absolute;top:-50px;right:-50px;width:200px;height:200px;background:radial-gradient(circle,var(--accent-d),transparent 70%);pointer-events:none}
.traf-main-label{font-size:10.5px;color:var(--t3);font-weight:700;text-transform:uppercase;letter-spacing:.08em;display:flex;align-items:center;gap:6px;margin-bottom:10px;position:relative;z-index:1}
.traf-main-val{font-size:34px;font-weight:800;color:var(--t1);line-height:1;letter-spacing:-.02em;display:flex;align-items:baseline;gap:6px;position:relative;z-index:1}
.traf-main-val span{font-size:14px;font-weight:500;color:var(--t3)}
.traf-trend{display:inline-flex;align-items:center;gap:4px;font-size:11px;font-weight:700;padding:4px 10px;border-radius:20px;margin-top:12px;position:relative;z-index:1}
.traf-trend.up{background:var(--green-bg);color:var(--green-t)}
.traf-trend.down{background:var(--red-bg);color:var(--red-t)}
.traf-mini{background:var(--card);border:1px solid var(--card-b);border-radius:20px;padding:18px 19px;display:flex;flex-direction:column;justify-content:space-between;transition:.2s}
.traf-mini:hover{border-color:var(--card-bh);transform:translateY(-2px)}
.traf-mini-top{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px}
.traf-mini-icon{width:32px;height:32px;border-radius:9px;background:var(--accent-d);color:var(--accent);display:flex;align-items:center;justify-content:center;font-size:15px}
.traf-mini-icon.pk{background:var(--amber-bg);color:var(--amber)}
.traf-mini-icon.lo{background:var(--purple-bg);color:var(--purple)}
.traf-mini-label{font-size:9.5px;color:var(--t3);font-weight:700;text-transform:uppercase;letter-spacing:.06em}
.traf-mini-val{font-size:21px;font-weight:800;color:var(--t1);letter-spacing:-.01em}
.traf-mini-sub{font-size:9.5px;color:var(--t3);margin-top:3px}

.traf-chart-card{background:var(--card);border:1px solid var(--card-b);border-radius:22px;padding:22px 24px 18px;box-shadow:var(--shadow);margin-bottom:16px}
.traf-chart-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:6px;flex-wrap:wrap;gap:10px}
.traf-chart-title{font-size:14px;font-weight:800;color:var(--t1);display:flex;align-items:center;gap:8px}
.traf-chart-title i{color:var(--accent);font-size:18px}
.traf-chart-sub{font-size:10.5px;color:var(--t3);margin-top:3px}
.traf-legend{display:flex;gap:14px;align-items:center}
.traf-legend-item{display:flex;align-items:center;gap:6px;font-size:10.5px;color:var(--t2);font-weight:600}
.traf-legend-dot{width:8px;height:8px;border-radius:3px}
.traf-range-tabs{display:flex;gap:4px;background:var(--accent-d);padding:3px;border-radius:10px;border:1px solid var(--card-b)}
.traf-range-tab{padding:6px 13px;border-radius:8px;font-size:10.5px;font-weight:700;color:var(--t3);cursor:pointer;transition:.15s;border:none;background:transparent;font-family:inherit}
.traf-range-tab.on{background:var(--accent);color:#fff;box-shadow:0 2px 8px rgba(111,156,240,.35)}
.traf-chart-body{height:320px;margin-top:14px;position:relative}

@media(max-width:900px){.traf-hero{grid-template-columns:1fr 1fr}}
@media(max-width:520px){.traf-hero{grid-template-columns:1fr}.traf-chart-body{height:260px}}
.m-icon{width:34px;height:34px;border-radius:8px;background:var(--accent-d);display:flex;align-items:center;justify-content:center;margin-bottom:11px;color:var(--accent);font-size:17px}
.m-icon.suc{background:var(--green-bg);color:var(--green)}
.m-icon.dan{background:var(--red-bg);color:var(--red)}
.m-icon.pur{background:var(--purple-bg);color:var(--purple)}
.m-label{font-size:10px;color:var(--t3);margin-bottom:4px;font-weight:600;text-transform:uppercase;letter-spacing:.05em}
.m-val{font-size:25px;font-weight:700;color:var(--t1);line-height:1;letter-spacing:-.02em}
.m-unit{font-size:12px;font-weight:400;color:var(--t3)}
.m-sub{font-size:10px;color:var(--t3);margin-top:6px;display:flex;align-items:center;gap:3px}
.vless-box{background:linear-gradient(135deg,var(--bg3) 0%,var(--bg2) 100%);border:1px solid var(--card-b);border-radius:18px;padding:20px 22px;margin-bottom:18px;box-shadow:var(--shadow);position:relative;overflow:hidden;transition:background .3s}
.vless-box::before{content:'';position:absolute;top:-50px;right:-50px;width:180px;height:180px;background:radial-gradient(circle,var(--accent-d),transparent 70%);pointer-events:none}
.vl-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:13px;flex-wrap:wrap;gap:8px}
.vl-title{color:var(--t2);font-size:11px;display:flex;align-items:center;gap:6px;font-weight:700;text-transform:uppercase;letter-spacing:.06em}
.vl-title i{color:var(--accent);font-size:15px}
.vl-code{background:rgba(0,0,0,.18);border:1px solid var(--card-b);border-radius:9px;padding:13px 15px;font-size:11px;font-family:IBM Plex Mono,ui-monospace,monospace;color:var(--accent2);word-break:break-all;line-height:1.8;letter-spacing:.01em}
[data-theme="light"] .vl-code{background:rgba(0,0,0,.04)}
.vl-actions{display:flex;gap:8px;margin-top:13px;flex-wrap:wrap}
.btn{font-family:inherit;font-size:12px;font-weight:500;border-radius:9px;padding:8px 14px;cursor:pointer;display:inline-flex;align-items:center;gap:5px;border:none;transition:all .15s;white-space:nowrap}
.btn i{font-size:13px}
.btn:disabled{opacity:.4;cursor:not-allowed}
.btn-p{background:linear-gradient(135deg,#2F8FFF,#8791a1);color:#fff;box-shadow:0 2px 14px rgba(135,145,161,.35)}
.btn-p:hover{background:#2563EB;box-shadow:0 4px 18px rgba(111,156,240,.4)}
.btn-o{background:transparent;border:1px solid var(--card-b);color:var(--t2)}
.btn-o:hover{background:var(--accent-d);border-color:rgba(111,156,240,.3)}
.btn-g{background:var(--accent-d);color:var(--accent2);border:1px solid rgba(111,156,240,.15)}
.btn-g:hover{background:rgba(111,156,240,.22)}
.btn-d{background:var(--red-bg);color:var(--red-t);border:1px solid rgba(239,68,68,.2)}
.btn-d:hover{background:rgba(239,68,68,.2)}
.btn-pur{background:var(--purple-bg);color:#a3acb9;border:1px solid rgba(135,145,161,.2)}
.btn-pur:hover{background:rgba(135,145,161,.22)}
.btn-amber{background:var(--amber-bg);color:var(--amber-t);border:1px solid rgba(245,158,11,.2)}
.btn-amber:hover{background:rgba(245,158,11,.22)}
.btn-sm{padding:5px 9px;font-size:10.5px;border-radius:7px}
.btn-icon{width:30px;height:30px;padding:0;justify-content:center;border-radius:5px}
.card{background:var(--card);border:1px solid var(--card-b);border-radius:var(--radius);padding:18px 20px;transition:border-color .2s,background .3s}
.card:hover{border-color:var(--card-bh)}
.card-title{font-size:12.5px;font-weight:700;color:var(--t1);margin-bottom:15px;display:flex;align-items:center;gap:7px}
.card-title i{font-size:16px;color:var(--accent)}
.ml-auto{margin-left:auto}
.g2{display:grid;grid-template-columns:1fr 1fr;gap:13px;margin-bottom:16px}
.g3{display:grid;grid-template-columns:2fr 1fr;gap:13px;margin-bottom:16px}
.mb16{margin-bottom:16px}
.sr{display:flex;align-items:center;justify-content:space-between;padding:9px 0;border-bottom:1px solid rgba(111,156,240,0.05);font-size:12px}
.sr:last-child{border-bottom:none}
.sr-k{color:var(--t2);display:flex;align-items:center;gap:6px}
.sr-k i{font-size:13px;color:var(--t3)}
.sr-v{color:var(--t1);font-weight:600;font-size:11.5px}
.ch{position:relative;height:230px}
.ch-lg{position:relative;height:330px}
.ch-sm{position:relative;height:185px}
.exp-chip{font-size:9px;padding:3px 8px;border-radius:6px;font-weight:700;display:inline-flex;align-items:center;gap:3px}
.ec-ok{background:var(--green-bg);color:var(--green-t)}
.ec-warn{background:var(--amber-bg);color:var(--amber-t)}
.ec-exp{background:var(--red-bg);color:var(--red-t)}
.ec-inf{background:var(--accent-d);color:var(--accent2)}
.tog{width:19px;height:34px;border-radius:19px;background:rgba(100,116,139,0.25);position:relative;cursor:pointer;transition:.2s;flex-shrink:0;border:none}
.tog::after{content:'';position:absolute;width:13px;height:13px;border-radius:50%;background:#fff;right:3px;bottom:3px;transition:.2s;box-shadow:0 1px 3px rgba(0,0,0,.3)}
.tog.on{background:var(--green)}
.tog.on::after{bottom:18px}
.form-row{display:flex;gap:9px;flex-wrap:wrap;align-items:flex-end}
.fg{display:flex;flex-direction:column;gap:5px}
.fg label{font-size:10px;color:var(--t3);font-weight:700;text-transform:uppercase;letter-spacing:.06em}
.fi,.fs{padding:9px 12px;border-radius:9px;border:1px solid var(--card-b);background:rgba(0,0,0,.18);color:var(--t1);font-family:inherit;font-size:12px;outline:none;transition:.15s;min-width:100px}
[data-theme="light"] .fi,[data-theme="light"] .fs{background:rgba(0,0,0,.04)}
.fi::placeholder{color:var(--t3)}
.fi:focus,.fs:focus{border-color:rgba(111,156,240,.45);background:rgba(0,0,0,.25);box-shadow:0 0 0 3px rgba(111,156,240,.08)}
.fs option{background:var(--bg2)}
[data-theme="light"] .fs option{background:#fff}
.cl{background:var(--accent-d);border:1px solid rgba(111,156,240,.15);border-radius:10px;padding:11px 13px;font-size:11px;color:var(--t2);display:flex;gap:9px;align-items:flex-start;line-height:1.8;margin-top:12px}
.cl i{font-size:15px;color:var(--accent);margin-top:1px;flex-shrink:0}
.cl.amber{background:var(--amber-bg);border-color:rgba(245,158,11,.2);color:var(--amber-t)}
/* ══════ پنل ساخت کانفیگ - طراحی جدید ══════ */
.create-panel{background:linear-gradient(155deg,var(--bg3) 0%,var(--card) 55%);border:1px solid var(--card-b);border-radius:22px;padding:0;overflow:hidden;box-shadow:var(--shadow);margin-bottom:16px;position:relative}
.create-panel::before{content:'';position:absolute;top:-60px;right:-60px;width:220px;height:220px;background:radial-gradient(circle,var(--accent-d),transparent 70%);pointer-events:none}
.cp-head{display:flex;align-items:center;gap:13px;padding:22px 24px 18px;position:relative;z-index:1}
.cp-head-icon{width:44px;height:44px;border-radius:13px;background:linear-gradient(135deg,var(--accent),var(--accent2));display:flex;align-items:center;justify-content:center;color:#fff;font-size:20px;flex-shrink:0;box-shadow:0 6px 18px rgba(111,156,240,.35)}
.cp-head-text{flex:1;min-width:0}
.cp-head-title{font-size:15px;font-weight:800;color:var(--t1);letter-spacing:-.01em}
.cp-head-sub{font-size:11px;color:var(--t3);margin-top:2px}
.cp-body{padding:2px 24px 22px;position:relative;z-index:1}
.cp-row{display:grid;grid-template-columns:1.3fr 1fr;gap:14px;margin-bottom:16px}
.cp-block{background:rgba(0,0,0,.14);border:1px solid var(--card-b);border-radius:14px;padding:14px 16px}
[data-theme="light"] .cp-block{background:rgba(37,99,235,.03)}
.cp-block-label{font-size:10px;font-weight:800;color:var(--t2);text-transform:uppercase;letter-spacing:.08em;display:flex;align-items:center;gap:6px;margin-bottom:11px}
.cp-block-label i{color:var(--accent);font-size:14px}
.cp-input-full{width:100%;padding:10px 13px;border-radius:10px;border:1px solid var(--card-b);background:rgba(0,0,0,.18);color:var(--t1);font-family:inherit;font-size:12.5px;outline:none;transition:.15s}
[data-theme="light"] .cp-input-full{background:#fff}
.cp-input-full:focus{border-color:rgba(111,156,240,.5);box-shadow:0 0 0 3px rgba(111,156,240,.1)}
.cp-input-full::placeholder{color:var(--t3)}
.cp-mini-row{display:flex;gap:8px;margin-top:9px}
.cp-quota-inputs{display:flex;gap:8px}
.cp-quota-inputs .cp-input-full{flex:1}
.cp-quota-inputs select.cp-input-full{flex:0 0 76px}
.chip-row{display:flex;gap:6px;flex-wrap:wrap;margin-top:9px}
.chip{font-size:10.5px;font-weight:700;padding:5px 12px;border-radius:8px;background:var(--accent-d);color:var(--t2);border:1px solid var(--card-b);cursor:pointer;transition:.15s;white-space:nowrap}
.chip:hover{background:rgba(111,156,240,.18);color:var(--accent2)}
.chip.active{background:var(--accent);color:#fff;border-color:var(--accent);box-shadow:0 3px 10px rgba(111,156,240,.35)}
.proto-cards{display:grid;grid-template-columns:repeat(3,1fr);gap:9px}
.proto-card{border:1.5px solid var(--card-b);border-radius:13px;padding:13px 12px;cursor:pointer;transition:.18s;text-align:center;position:relative;background:rgba(0,0,0,.1)}
[data-theme="light"] .proto-card{background:#fff}
.proto-card:hover{border-color:var(--card-bh);transform:translateY(-1px)}
.proto-card.active{border-color:var(--accent);background:var(--accent-d);box-shadow:0 0 0 3px rgba(111,156,240,.1)}
.proto-card.active .proto-card-check{opacity:1;transform:scale(1)}
.proto-card-check{position:absolute;top:7px;right:7px;width:16px;height:16px;border-radius:50%;background:var(--accent);color:#fff;font-size:10px;display:flex;align-items:center;justify-content:center;opacity:0;transform:scale(.5);transition:.18s}
.proto-card-icon{width:32px;height:32px;border-radius:9px;background:var(--accent-d);color:var(--accent);display:flex;align-items:center;justify-content:center;font-size:16px;margin:0 auto 8px}
.proto-card.active .proto-card-icon{background:var(--accent);color:#fff}
.proto-card-title{font-size:11px;font-weight:800;color:var(--t1)}
.proto-card-desc{font-size:9px;color:var(--t3);margin-top:3px;line-height:1.5}
.cp-footer{display:flex;align-items:center;justify-content:space-between;gap:12px;padding-top:16px;border-top:1px solid var(--card-b);flex-wrap:wrap}
.cp-footer-note{display:flex;align-items:center;gap:8px;font-size:10.5px;color:var(--t3);line-height:1.7;flex:1;min-width:220px}
.cp-footer-note i{color:var(--accent);font-size:15px;flex-shrink:0}
.cp-submit-btn{background:linear-gradient(135deg,var(--accent),var(--accent2));color:#fff;border:none;border-radius:13px;padding:13px 26px;font-family:inherit;font-size:13px;font-weight:800;cursor:pointer;display:flex;align-items:center;gap:8px;box-shadow:0 6px 20px rgba(111,156,240,.35);transition:.18s;white-space:nowrap}
.cp-submit-btn:hover{transform:translateY(-2px);box-shadow:0 10px 26px rgba(111,156,240,.45)}
.cp-submit-btn:active{transform:translateY(0) scale(.98)}
@media(max-width:760px){
  .cp-row{grid-template-columns:1fr}
  .proto-cards{grid-template-columns:1fr}
  .cp-footer{flex-direction:column;align-items:stretch}
  .cp-submit-btn{justify-content:center}
}
/* ══════ پنل اطلاعات سرور ══════ */
.srv-panel{background:linear-gradient(155deg,var(--bg3) 0%,var(--card) 60%);border:1px solid var(--card-b);border-radius:22px;overflow:hidden;box-shadow:var(--shadow);position:relative}
.srv-panel::before{content:'';position:absolute;top:-60px;right:-60px;width:200px;height:200px;background:radial-gradient(circle,var(--accent-d),transparent 70%);pointer-events:none}
.srv-hero{display:flex;align-items:center;gap:14px;padding:22px 24px;position:relative;z-index:1;border-bottom:1px solid var(--card-b)}
.srv-hero-icon{width:50px;height:50px;border-radius:14px;background:linear-gradient(135deg,var(--accent),var(--accent2));display:flex;align-items:center;justify-content:center;color:#fff;font-size:22px;flex-shrink:0;box-shadow:0 6px 18px rgba(111,156,240,.35)}
.srv-hero-text{flex:1;min-width:0}
.srv-hero-domain{font-size:15px;font-weight:800;color:var(--t1);word-break:break-all}
.srv-hero-sub{font-size:10.5px;color:var(--t3);margin-top:4px;display:flex;align-items:center;gap:6px}
.srv-tiles{display:grid;grid-template-columns:1fr 1fr;gap:11px;padding:20px 22px 22px;position:relative;z-index:1}
.srv-tile{display:flex;align-items:center;gap:11px;background:rgba(0,0,0,.14);border:1px solid var(--card-b);border-radius:13px;padding:12px 14px;transition:.18s}
[data-theme="light"] .srv-tile{background:rgba(37,99,235,.03)}
.srv-tile:hover{border-color:var(--card-bh);transform:translateY(-1px)}
.srv-tile-icon{width:34px;height:34px;border-radius:10px;background:var(--accent-d);color:var(--accent);display:flex;align-items:center;justify-content:center;font-size:16px;flex-shrink:0}
.srv-tile-text{min-width:0}
.srv-tile-label{font-size:9.5px;color:var(--t3);font-weight:700;text-transform:uppercase;letter-spacing:.05em;margin-bottom:3px}
.srv-tile-val{font-size:12px;font-weight:700;color:var(--t1);word-break:break-word}

/* ══════ پنل تغییر رمز ══════ */
.pw-panel{background:linear-gradient(155deg,var(--bg3) 0%,var(--card) 60%);border:1px solid var(--card-b);border-radius:22px;overflow:hidden;box-shadow:var(--shadow);position:relative}
.pw-panel::before{content:'';position:absolute;top:-60px;left:-60px;width:200px;height:200px;background:radial-gradient(circle,var(--purple-bg),transparent 70%);pointer-events:none}
.pw-hero{display:flex;align-items:center;gap:14px;padding:22px 24px 18px;position:relative;z-index:1}
.pw-hero-icon{width:50px;height:50px;border-radius:14px;background:linear-gradient(135deg,var(--purple),#6D48D6);display:flex;align-items:center;justify-content:center;color:#fff;font-size:22px;flex-shrink:0;box-shadow:0 6px 18px rgba(135,145,161,.35)}
.pw-hero-text{flex:1;min-width:0}
.pw-hero-title{font-size:15px;font-weight:800;color:var(--t1)}
.pw-hero-sub{font-size:10.5px;color:var(--t3);margin-top:3px}
.pw-body{padding:2px 24px 22px;position:relative;z-index:1}
.pw-field{position:relative;margin-bottom:13px}
.pw-field label{display:block;font-size:10px;font-weight:700;color:var(--t2);text-transform:uppercase;letter-spacing:.06em;margin-bottom:7px}
.pw-input{width:100%;padding:11px 14px 11px 42px;border-radius:11px;border:1px solid var(--card-b);background:rgba(0,0,0,.18);color:var(--t1);font-family:inherit;font-size:12.5px;outline:none;transition:.15s}
[data-theme="light"] .pw-input{background:#fff}
.pw-input:focus{border-color:rgba(135,145,161,.5);box-shadow:0 0 0 3px rgba(135,145,161,.1)}
.pw-eye{position:absolute;right:12px;top:34px;background:none;border:none;color:var(--t3);cursor:pointer;font-size:16px;padding:4px;display:flex}
.pw-eye:hover{color:var(--purple)}
.pw-strength{height:4px;border-radius:3px;background:var(--accent-d);margin-top:8px;overflow:hidden;display:flex;gap:3px}
.pw-strength-seg{flex:1;height:100%;border-radius:3px;background:rgba(100,116,139,.2);transition:.25s}
.pw-strength-label{font-size:9.5px;color:var(--t3);margin-top:5px;display:flex;align-items:center;gap:5px}
.pw-reqs{display:flex;flex-wrap:wrap;gap:6px;margin-top:11px;margin-bottom:16px}
.pw-req{font-size:9.5px;padding:4px 10px;border-radius:7px;background:var(--accent-d);color:var(--t3);font-weight:600;display:flex;align-items:center;gap:4px;transition:.18s}
.pw-req.met{background:var(--green-bg);color:var(--green-t)}
.pw-submit{width:100%;justify-content:center;background:linear-gradient(135deg,var(--purple),#6D48D6);color:#fff;border:none;border-radius:12px;padding:12px;font-family:inherit;font-size:13px;font-weight:800;cursor:pointer;display:flex;align-items:center;gap:8px;box-shadow:0 6px 18px rgba(135,145,161,.32);transition:.18s}
.pw-submit:hover{transform:translateY(-2px);box-shadow:0 10px 24px rgba(135,145,161,.42)}
.pw-submit:active{transform:translateY(0) scale(.98)}

/* ══════ اتصالات فعال - نسخه پیشرفته ══════ */
.conn-hero{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:18px}
.conn-hero-tile{background:var(--card);border:1px solid var(--card-b);border-radius:16px;padding:16px 18px;position:relative;overflow:hidden;transition:.2s}
.conn-hero-tile:hover{border-color:var(--card-bh);transform:translateY(-2px);box-shadow:var(--shadow)}
.conn-hero-tile::after{content:'';position:absolute;bottom:0;right:0;left:0;height:2px;background:linear-gradient(90deg,var(--green),transparent)}
.conn-hero-icon{width:32px;height:32px;border-radius:9px;background:var(--green-bg);color:var(--green-t);display:flex;align-items:center;justify-content:center;font-size:15px;margin-bottom:10px}
.conn-hero-tile:nth-child(2) .conn-hero-icon{background:var(--accent-d);color:var(--accent)}
.conn-hero-tile:nth-child(3) .conn-hero-icon{background:var(--purple-bg);color:var(--purple)}
.conn-hero-tile:nth-child(4) .conn-hero-icon{background:var(--amber-bg);color:var(--amber)}
.conn-hero-label{font-size:9.5px;color:var(--t3);font-weight:700;text-transform:uppercase;letter-spacing:.06em;margin-bottom:4px}
.conn-hero-val{font-size:21px;font-weight:800;color:var(--t1);line-height:1;letter-spacing:-.02em}
.conn-hero-unit{font-size:11px;color:var(--t3);font-weight:500}

.conn-toolbar{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:14px;flex-wrap:wrap}
.conn-toolbar-title{font-size:12px;font-weight:800;color:var(--t2);display:flex;align-items:center;gap:7px;text-transform:uppercase;letter-spacing:.06em}
.conn-toolbar-title i{color:var(--green);font-size:15px}
.conn-live-badge{display:flex;align-items:center;gap:6px;font-size:10.5px;font-weight:700;color:var(--green-t);background:var(--green-bg);padding:5px 12px;border-radius:20px;border:1px solid rgba(16,185,129,.2)}
.conn-live-dot{width:6px;height:6px;border-radius:50%;background:var(--green);animation:pulse 1.6s infinite}

.conn-grid-v2{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px}
.conn-card-v2{background:var(--card);border:1px solid var(--card-b);border-radius:18px;padding:0;overflow:hidden;transition:all .22s cubic-bezier(.4,0,.2,1);position:relative}
.conn-card-v2:hover{border-color:var(--card-bh);transform:translateY(-3px);box-shadow:0 14px 32px rgba(0,0,0,.22)}
.conn-card-v2-glow{position:absolute;top:-40px;right:-40px;width:140px;height:140px;background:radial-gradient(circle,rgba(16,185,129,.1),transparent 70%);pointer-events:none}
.conn-card-v2-top{display:flex;align-items:center;gap:12px;padding:16px 17px 13px;position:relative;z-index:1}
.conn-avatar{width:42px;height:42px;border-radius:13px;background:linear-gradient(135deg,var(--green),#0D9668);display:flex;align-items:center;justify-content:center;color:#fff;font-size:18px;flex-shrink:0;position:relative;box-shadow:0 4px 14px rgba(16,185,129,.3)}
.conn-avatar::after{content:'';position:absolute;inset:-4px;border-radius:16px;border:1.5px solid var(--green);opacity:.4;animation:breathe2 2.4s ease-in-out infinite}
@keyframes breathe2{0%,100%{transform:scale(1);opacity:.4}50%{transform:scale(1.12);opacity:0}}
.conn-card-v2-id{flex:1;min-width:0}
.conn-ip-v2{font-family:IBM Plex Mono,ui-monospace,monospace;font-size:14px;font-weight:800;color:var(--t1);display:flex;align-items:center;gap:6px}
.conn-ip-copy{background:none;border:none;color:var(--t3);cursor:pointer;font-size:12px;padding:2px;display:flex;transition:.15s}
.conn-ip-copy:hover{color:var(--accent)}
.conn-label-v2{font-size:10.5px;color:var(--t3);margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.conn-status-pill{font-size:9px;font-weight:800;padding:4px 9px;border-radius:20px;background:var(--green-bg);color:var(--green-t);display:flex;align-items:center;gap:4px;white-space:nowrap;flex-shrink:0}
.conn-card-v2-divider{height:1px;background:linear-gradient(90deg,transparent,var(--card-b) 15%,var(--card-b) 85%,transparent);margin:0 17px}
.conn-card-v2-body{padding:14px 17px 16px}
.conn-proto-row{margin-bottom:12px}
.conn-stat-row{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:12px}
.conn-stat-box{display:flex;align-items:center;gap:8px}
.conn-stat-icon{width:26px;height:26px;border-radius:8px;background:var(--accent-d);color:var(--accent);display:flex;align-items:center;justify-content:center;font-size:12px;flex-shrink:0}
.conn-stat-icon.time{background:var(--purple-bg);color:var(--purple)}
.conn-stat-text-label{font-size:8.5px;color:var(--t3);font-weight:700;text-transform:uppercase;letter-spacing:.04em}
.conn-stat-text-val{font-size:11.5px;font-weight:700;color:var(--t1);margin-top:1px}
.conn-duration-track{height:5px;border-radius:4px;background:var(--accent-d);overflow:hidden;position:relative}
.conn-duration-fill{height:100%;border-radius:4px;background:linear-gradient(90deg,var(--green),#3FD79C);position:relative;overflow:hidden}
.conn-duration-fill::after{content:'';position:absolute;inset:0;background:linear-gradient(90deg,transparent,rgba(255,255,255,.35),transparent);width:40%;animation:shimmer 1.8s linear infinite}
@keyframes shimmer{0%{transform:translateX(-120%)}100%{transform:translateX(280%)}}

.conn-empty-v2{text-align:center;padding:70px 20px;background:var(--card);border:1px dashed var(--card-b);border-radius:20px}
.conn-empty-v2-icon{width:64px;height:64px;border-radius:18px;background:var(--accent-d);display:flex;align-items:center;justify-content:center;font-size:28px;color:var(--t3);margin:0 auto 16px}
.conn-empty-v2-title{font-size:13.5px;font-weight:700;color:var(--t2);margin-bottom:5px}
.conn-empty-v2-sub{font-size:11px;color:var(--t3)}

@media(max-width:760px){.conn-hero{grid-template-columns:1fr 1fr}}
@media(max-width:500px){.conn-grid-v2{grid-template-columns:1fr}}

@media(max-width:560px){.srv-tiles{grid-template-columns:1fr}}
.cl.amber i{color:var(--amber)}
.sub-box{background:rgba(135,145,161,.07);border:1px solid rgba(135,145,161,.2);border-radius:10px;padding:14px 16px;display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap;margin-top:11px}
.sub-url{font-family:IBM Plex Mono,ui-monospace,monospace;font-size:10.5px;color:#a3acb9;word-break:break-all;flex:1}
.spbar{height:4px;border-radius:3px;background:var(--accent-d);margin-top:5px;overflow:hidden}
.spfill{height:100%;border-radius:3px;background:linear-gradient(90deg,var(--accent),var(--accent2));transition:width 1s}
.empty{text-align:center;padding:50px 20px;color:var(--t3)}
.empty i{font-size:40px;opacity:.3;margin-bottom:12px;display:block}
.empty p{font-size:12.5px;margin-top:4px}
/* ══════ گروه‌های ساب - ریدیزاین کامل ══════ */
.subs-toolbar{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:16px;flex-wrap:wrap}
.subs-search{flex:1;min-width:200px;position:relative}
.subs-search input{width:100%;padding:11px 15px 11px 40px;border-radius:12px;border:1px solid var(--card-b);background:var(--card);color:var(--t1);font-family:inherit;font-size:12.5px;outline:none;transition:.15s}
.subs-search input:focus{border-color:rgba(135,145,161,.5);box-shadow:0 0 0 3px rgba(135,145,161,.1)}
.subs-search i{position:absolute;right:14px;top:50%;transform:translateY(-50%);color:var(--t3);font-size:15px}

.sub-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:16px;margin-bottom:18px}
.sub-card{background:var(--card);border:1px solid var(--card-b);border-radius:20px;padding:0;overflow:hidden;transition:all .25s cubic-bezier(.4,0,.2,1);position:relative}
.sub-card:hover{border-color:var(--card-bh);transform:translateY(-4px);box-shadow:0 16px 36px rgba(0,0,0,.24)}
.sub-card-top{background:linear-gradient(155deg,var(--purple-bg) 0%,transparent 65%);padding:20px 20px 16px;position:relative}
.sub-card-top::before{content:'';position:absolute;top:-30px;right:-30px;width:130px;height:130px;background:radial-gradient(circle,rgba(135,145,161,.14),transparent 70%);pointer-events:none}
.sub-card-head-v2{display:flex;align-items:flex-start;gap:13px;position:relative;z-index:1}
.sub-card-icon{width:46px;height:46px;border-radius:14px;background:linear-gradient(135deg,var(--purple),#6D48D6);display:flex;align-items:center;justify-content:center;color:#fff;font-size:20px;flex-shrink:0;box-shadow:0 6px 16px rgba(135,145,161,.35)}
.sub-card-titles{flex:1;min-width:0}
.sub-card-name-v2{font-size:15.5px;font-weight:800;color:var(--t1);letter-spacing:-.01em;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.sub-card-desc-v2{font-size:11px;color:var(--t3);margin-top:3px;line-height:1.6;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.sub-card-lock-badge{flex-shrink:0;width:26px;height:26px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:12px}
.sub-card-lock-badge.locked{background:var(--amber-bg);color:var(--amber-t)}
.sub-card-lock-badge.open{background:var(--green-bg);color:var(--green-t)}

.sub-card-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:0;position:relative;z-index:1;margin-top:16px;background:rgba(0,0,0,.14);border:1px solid var(--card-b);border-radius:13px;overflow:hidden}
[data-theme="light"] .sub-card-stats{background:rgba(95,107,125,.03)}
.sub-card-stat{padding:11px 8px;text-align:center;border-right:1px solid var(--card-b)}
.sub-card-stat:last-child{border-right:none}
.sub-card-stat-val{font-size:15px;font-weight:800;color:var(--t1);line-height:1.2}
.sub-card-stat-label{font-size:8.5px;color:var(--t3);font-weight:700;text-transform:uppercase;letter-spacing:.05em;margin-top:4px}

.sub-card-url-row{margin:14px 20px 0;background:rgba(135,145,161,.08);border:1px dashed rgba(135,145,161,.25);border-radius:11px;padding:9px 12px;display:flex;align-items:center;gap:8px}
.sub-card-url-text{font-family:IBM Plex Mono,ui-monospace,monospace;font-size:9.5px;color:#a3acb9;flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.sub-card-url-copy{background:none;border:none;color:var(--purple);cursor:pointer;font-size:13px;padding:3px;display:flex;flex-shrink:0;transition:.15s}
.sub-card-url-copy:hover{color:#a3acb9;transform:scale(1.1)}

.sub-card-bottom{padding:14px 20px 18px;display:flex;gap:7px;flex-wrap:wrap}
.sub-card-bottom .btn{flex:1;justify-content:center;min-width:fit-content}

.subs-empty-v2{text-align:center;padding:70px 20px;background:var(--card);border:1px dashed var(--card-b);border-radius:20px;grid-column:1/-1}
.subs-empty-v2-icon{width:64px;height:64px;border-radius:18px;background:var(--purple-bg);display:flex;align-items:center;justify-content:center;font-size:28px;color:var(--purple);margin:0 auto 16px}
.subs-empty-v2-title{font-size:13.5px;font-weight:700;color:var(--t2);margin-bottom:5px}
.subs-empty-v2-sub{font-size:11px;color:var(--t3)}

/* ══════ مودال ساخت گروه - نسخه فشرده ══════ */
.modal-v2{background:var(--card);border:1px solid var(--card-b);border-radius:22px;padding:0;max-width:430px;width:calc(100% - 32px);max-height:92vh;overflow-y:auto;position:relative;animation:fi .2s ease;box-shadow:0 24px 70px rgba(0,0,0,.5)}
.modal-v2-head{background:linear-gradient(155deg,rgba(135,145,161,.14) 0%,transparent 65%);padding:18px 22px 14px;position:relative;overflow:hidden}
.modal-v2-head::before{content:'';position:absolute;top:-50px;right:-50px;width:160px;height:160px;background:radial-gradient(circle,rgba(135,145,161,.2),transparent 70%);pointer-events:none}
.modal-v2-close{position:absolute;top:14px;right:14px;background:var(--accent-d);border:1px solid var(--card-b);color:var(--t2);width:30px;height:30px;border-radius:9px;font-size:15px;display:flex;align-items:center;justify-content:center;cursor:pointer;z-index:2;transition:.15s}
.modal-v2-close:hover{background:var(--red-bg);color:var(--red-t);border-color:rgba(239,68,68,.25)}
.modal-v2-icon{width:42px;height:42px;border-radius:13px;background:linear-gradient(135deg,var(--purple),#6D48D6);display:flex;align-items:center;justify-content:center;color:#fff;font-size:19px;margin-bottom:10px;position:relative;z-index:1;box-shadow:0 8px 18px rgba(135,145,161,.4)}
.modal-v2-title{font-size:15.5px;font-weight:800;color:var(--t1);position:relative;z-index:1;letter-spacing:-.01em}
.modal-v2-sub{font-size:10.5px;color:var(--t3);margin-top:3px;position:relative;z-index:1;line-height:1.6}
.modal-v2-body{padding:16px 22px 20px;border-top:1px solid var(--card-b)}
.modal-v2-field{margin-bottom:11px}
.modal-v2-field label{display:flex;align-items:center;gap:5px;font-size:9.5px;font-weight:800;color:var(--t2);text-transform:uppercase;letter-spacing:.06em;margin-bottom:6px}
.modal-v2-field label i{color:var(--purple);font-size:13px}
.modal-v2-input-wrap{position:relative}
.modal-v2-input-wrap>i{position:absolute;left:13px;top:50%;transform:translateY(-50%);color:var(--t3);font-size:14px;pointer-events:none;transition:.15s;z-index:1}
.modal-v2-input{width:100%;padding:9px 13px 9px 38px;border-radius:11px;border:1px solid var(--card-b);background:rgba(0,0,0,.2);color:var(--t1);font-family:inherit;font-size:12.5px;outline:none;transition:.18s}
[data-theme="light"] .modal-v2-input{background:rgba(95,107,125,.04)}
.modal-v2-input::placeholder{color:var(--t3)}
.modal-v2-input:focus{border-color:rgba(135,145,161,.55);box-shadow:0 0 0 3px rgba(135,145,161,.12);background:rgba(0,0,0,.28)}
[data-theme="light"] .modal-v2-input:focus{background:#fff}
.modal-v2-input:focus~i{color:var(--purple)}
.modal-v2-hint{background:rgba(111,156,240,.08);border:1px solid rgba(111,156,240,.18);border-radius:11px;padding:9px 12px;font-size:10px;color:var(--t2);display:flex;gap:7px;align-items:flex-start;line-height:1.6;margin-top:2px}
.modal-v2-hint i{font-size:14px;color:var(--accent);margin-top:1px;flex-shrink:0}
.modal-v2-footer{display:flex;gap:8px;margin-top:15px}
.modal-v2-btn-cancel{flex:.75;justify-content:center;padding:10px;border-radius:11px;background:transparent;border:1px solid var(--card-b);color:var(--t2);font-family:inherit;font-size:12px;font-weight:700;cursor:pointer;transition:.15s;display:flex;align-items:center}
.modal-v2-btn-cancel:hover{background:var(--accent-d);color:var(--t1)}
.modal-v2-btn-submit{flex:1;justify-content:center;padding:10px;border-radius:11px;background:linear-gradient(135deg,var(--purple),#6D48D6);color:#fff;border:none;font-family:inherit;font-size:12px;font-weight:800;cursor:pointer;display:flex;align-items:center;gap:6px;box-shadow:0 6px 18px rgba(135,145,161,.4);transition:.18s}
.modal-v2-btn-submit:hover{transform:translateY(-2px);box-shadow:0 10px 24px rgba(135,145,161,.5)}
.modal-v2-btn-submit:active{transform:translateY(0) scale(.98)}

/* ══════ مودال انتخاب کانفیگ - نسخه پیشرفته ══════ */
.lmodal-head{background:linear-gradient(155deg,var(--accent-d) 0%,transparent 70%);padding:22px 24px 18px;position:relative;border-bottom:1px solid var(--card-b)}
.lmodal-icon-row{display:flex;align-items:center;gap:12px;position:relative;z-index:1}
.lmodal-icon{width:44px;height:44px;border-radius:13px;background:linear-gradient(135deg,var(--accent),var(--accent2));display:flex;align-items:center;justify-content:center;color:#fff;font-size:19px;flex-shrink:0;box-shadow:0 6px 16px rgba(111,156,240,.35)}
.lmodal-title-v2{font-size:14.5px;font-weight:800;color:var(--t1)}
.lmodal-sub-v2{font-size:10.5px;color:var(--t3);margin-top:2px}
.lmodal-search{margin-top:14px;position:relative}
.lmodal-search input{width:100%;padding:10px 13px 10px 38px;border-radius:11px;border:1px solid var(--card-b);background:rgba(0,0,0,.2);color:var(--t1);font-family:inherit;font-size:12px;outline:none}
[data-theme="light"] .lmodal-search input{background:#fff}
.lmodal-search input:focus{border-color:rgba(111,156,240,.5);box-shadow:0 0 0 3px rgba(111,156,240,.1)}
.lmodal-search i{position:absolute;right:12px;top:50%;transform:translateY(-50%);color:var(--t3);font-size:14px}
.lmodal-quickbar{display:flex;gap:8px;margin-top:11px;position:relative;z-index:1}
.lmodal-qbtn{font-size:10px;font-weight:700;padding:5px 11px;border-radius:8px;background:var(--accent-d);color:var(--accent2);border:1px solid var(--card-b);cursor:pointer;transition:.15s;font-family:inherit}
.lmodal-qbtn:hover{background:rgba(111,156,240,.2)}
.lmodal-count{margin-left:auto;font-size:10.5px;color:var(--t3);display:flex;align-items:center}

.lmodal-list{padding:10px 14px;max-height:360px;overflow-y:auto}
.lrow-v2{display:flex;align-items:center;gap:11px;padding:11px 12px;border-radius:13px;cursor:pointer;transition:.15s;margin-bottom:4px;border:1px solid transparent}
.lrow-v2:hover{background:var(--accent-d)}
.lrow-v2.checked{background:rgba(111,156,240,.1);border-color:rgba(111,156,240,.25)}
.lrow-v2-check{width:20px;height:20px;border-radius:7px;border:2px solid var(--card-b);flex-shrink:0;display:flex;align-items:center;justify-content:center;transition:.15s;background:rgba(0,0,0,.14)}
.lrow-v2.checked .lrow-v2-check{background:var(--accent);border-color:var(--accent)}
.lrow-v2-check i{font-size:12px;color:#fff;opacity:0;transform:scale(.5);transition:.15s}
.lrow-v2.checked .lrow-v2-check i{opacity:1;transform:scale(1)}
.lrow-v2-avatar{width:34px;height:34px;border-radius:10px;background:var(--accent-d);color:var(--accent);display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0}
.lrow-v2.checked .lrow-v2-avatar{background:var(--accent);color:#fff}
.lrow-v2-info{flex:1;min-width:0}
.lrow-v2-name{font-size:12.5px;font-weight:700;color:var(--t1);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.lrow-v2-meta{font-size:9.5px;color:var(--t3);margin-top:2px;display:flex;align-items:center;gap:6px}
.lrow-v2-status{font-size:9px;font-weight:800;padding:3px 9px;border-radius:20px;flex-shrink:0;white-space:nowrap}
.lrow-v2-status.on{background:var(--green-bg);color:var(--green-t)}
.lrow-v2-status.off{background:var(--red-bg);color:var(--red-t)}

.lmodal-footer{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:16px 24px;border-top:1px solid var(--card-b)}
.lmodal-footer-info{font-size:10.5px;color:var(--t3);display:flex;align-items:center;gap:6px}
.lmodal-footer-info i{color:var(--accent)}
.lmodal-footer-btns{display:flex;gap:8px}

@media(max-width:500px){.sub-grid{grid-template-columns:1fr}.sub-card-stats{grid-template-columns:repeat(3,1fr)}}

.modal-bg{display:none;position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:500;align-items:center;justify-content:center;backdrop-filter:blur(4px)}
.modal-bg.open{display:flex}
.modal{background:var(--card);border:1px solid var(--card-b);border-radius:20px;padding:28px 26px;max-width:520px;width:calc(100% - 32px);max-height:90vh;overflow-y:auto;position:relative;animation:fi .2s ease}
.modal-close{position:absolute;top:14px;right:14px;background:var(--accent-d);border:1px solid var(--card-b);color:var(--t2);width:30px;height:30px;border-radius:8px;font-size:16px;display:flex;align-items:center;justify-content:center;cursor:pointer;border:none}
.modal-title{font-size:16px;font-weight:700;color:var(--t1);margin-bottom:18px;display:flex;align-items:center;gap:8px}
.modal-title i{color:var(--accent)}
.lrow{display:flex;align-items:center;gap:8px;padding:7px 0;border-bottom:1px solid rgba(111,156,240,.05)}
.lrow:last-child{border-bottom:none}
.lrow-check{width:16px;height:16px;border-radius:4px;cursor:pointer;accent-color:var(--accent)}
.lrow-label{flex:1;font-size:12px;color:var(--t1)}
.lrow-badge{font-size:9px;padding:2px 7px;border-radius:5px;background:var(--green-bg);color:var(--green-t);font-weight:700}
.toast{position:fixed;bottom:22px;left:50%;transform:translateX(-50%) translateY(40px);background:var(--card);border:1px solid var(--card-b);color:var(--t1);border-radius:10px;padding:10px 18px;font-size:12.5px;opacity:0;transition:all .25s;z-index:999;pointer-events:none;display:flex;align-items:center;gap:8px;box-shadow:var(--shadow);white-space:nowrap}
.toast.show{opacity:1;transform:translateX(-50%) translateY(0)}
.toast.ok{border-color:rgba(16,185,129,.3);background:var(--green-bg);color:var(--green-t)}
.toast.err{border-color:rgba(239,68,68,.3);background:var(--red-bg);color:var(--red-t)}
.dash-footer{border-top:1px solid var(--card-b);margin-top:14px;padding-top:14px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px}
.df-text{font-size:10px;color:var(--t3)}
.df-link{font-size:11.5px;color:var(--accent2);display:flex;align-items:center;gap:5px;font-weight:600}

/* ══════ کانفیگ‌ها - طراحی ردیفی حرفه‌ای ══════ */
.cfg-grid{display:flex;flex-direction:column;gap:10px}
.cfg-card{background:var(--card);border:1px solid var(--card-b);border-radius:14px;padding:0;transition:all .2s cubic-bezier(.4,0,.2,1);position:relative;overflow:hidden}
.cfg-card:hover{border-color:var(--card-bh);box-shadow:0 6px 24px rgba(0,0,0,.18)}
.cfg-card.is-off{opacity:.6}
.cfg-card.is-exp{opacity:.78}
.cfg-row{display:flex;align-items:center;gap:16px;padding:14px 18px}
.cfg-status-dot{width:9px;height:9px;border-radius:50%;background:var(--green);flex-shrink:0;box-shadow:0 0 0 3px var(--green-bg)}
.cfg-card.is-off .cfg-status-dot{background:var(--red);box-shadow:0 0 0 3px var(--red-bg)}
.cfg-card.is-exp .cfg-status-dot{background:var(--amber);box-shadow:0 0 0 3px var(--amber-bg)}
.cfg-identity{display:flex;flex-direction:column;gap:3px;min-width:150px;flex-shrink:0}
.cfg-label{font-size:13.5px;font-weight:700;color:var(--t1);display:flex;align-items:center;gap:7px}
.cfg-sub-meta{display:flex;align-items:center;gap:8px;font-size:10px;color:var(--t3)}
.cfg-uuid-mini{font-family:IBM Plex Mono,ui-monospace,monospace;font-size:9.5px;color:var(--accent2);background:var(--accent-d);padding:2px 7px;border-radius:5px;cursor:pointer;transition:.15s}
.cfg-uuid-mini:hover{background:rgba(111,156,240,.2)}
.cfg-divider-v{width:1px;align-self:stretch;background:var(--card-b);flex-shrink:0}
.cfg-usage-col{flex:1;min-width:160px;display:flex;flex-direction:column;gap:5px}
.ubar{height:5px;border-radius:4px;background:rgba(111,156,240,0.1);overflow:hidden}
.ubar-f{height:100%;border-radius:4px;transition:width .4s ease}
.utxt{font-size:10px;color:var(--t3);display:flex;justify-content:space-between}
.cfg-exp-col{flex-shrink:0;min-width:110px}
.cfg-badges-col{display:flex;flex-direction:column;gap:5px;flex-shrink:0;align-items:flex-end}
.cfg-actions{display:flex;gap:5px;flex-shrink:0}
.links-toolbar{display:flex;align-items:center;gap:14px;margin-bottom:12px;flex-wrap:wrap}
.bulk-selall{display:flex;align-items:center;gap:7px;font-size:12px;color:var(--t2);cursor:pointer;user-select:none;flex-shrink:0}
.bulk-selall input{width:16px;height:16px;accent-color:var(--accent);cursor:pointer}
.bulk-bar{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;background:var(--card);border:1px solid var(--card-b);border-radius:14px;padding:10px 16px;margin-bottom:12px}
.bulk-count{font-size:12.5px;font-weight:700;color:var(--t1);display:flex;align-items:center;gap:6px}
.bulk-actions{display:flex;gap:6px;flex-wrap:wrap}
.cfg-select{display:flex;align-items:center;flex-shrink:0}
.cfg-select input{width:17px;height:17px;accent-color:var(--accent);cursor:pointer}
.proto-chip{font-size:9px;padding:3px 8px;border-radius:6px;font-weight:700;white-space:nowrap}
.pc-ws{background:var(--accent-d);color:var(--accent2)}
.pc-xhttp{background:var(--purple-bg);color:#a3acb9}
.pc-ultra{background:var(--green-bg);color:var(--green-t)}
.cfg-sub-tag{font-size:9.5px;color:var(--t3);display:flex;align-items:center;gap:4px;white-space:nowrap}
.cfg-sub-tag i{color:var(--purple);font-size:11px}
.tog{width:19px;height:30px;border-radius:19px;background:rgba(100,116,139,0.25);position:relative;cursor:pointer;transition:.2s;flex-shrink:0;border:none}
.tog::after{content:'';position:absolute;width:13px;height:13px;border-radius:50%;background:#fff;right:3px;top:3px;transition:.2s;box-shadow:0 1px 3px rgba(0,0,0,.3)}
.tog.on::after{top:14px}
.tog.on{background:var(--green)}

@media(max-width:880px){
  .cfg-row{flex-wrap:wrap}
  .cfg-divider-v{display:none}
  .cfg-usage-col{min-width:100%;order:5}
}

/* ── زیر ۷۶۸px: تبدیل کامل به کارت موبایل ── */
@media(max-width:768px){
  .cfg-grid{display:grid;grid-template-columns:1fr;gap:13px}
  .cfg-card{border-radius:16px}
  .cfg-row{flex-direction:column;align-items:stretch;gap:12px;padding:16px}
  .cfg-row-top{display:flex;align-items:center;justify-content:space-between;gap:10px}
  .cfg-identity{min-width:0;flex:1}
  .cfg-usage-col{min-width:0}
  .cfg-exp-col{min-width:0}
  .cfg-badges-col{flex-direction:row;align-items:center;flex-wrap:wrap}
  .cfg-actions{flex-wrap:wrap;border-top:1px solid var(--card-b);padding-top:10px;margin-top:2px;width:100%}
}

/* ══════ اتصالات فعال با IP ══════ */
.conn-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px}
.conn-card{background:var(--card);border:1px solid var(--card-b);border-radius:16px;padding:15px 17px;transition:.2s;position:relative;overflow:hidden}
.conn-card:hover{border-color:var(--card-bh);transform:translateY(-1px)}
.conn-card::before{content:'';position:absolute;top:0;left:0;width:3px;height:100%;background:var(--green)}
.conn-ip-row{display:flex;align-items:center;gap:8px;margin-bottom:10px}
.conn-ip-icon{width:32px;height:32px;border-radius:9px;background:var(--green-bg);color:var(--green-t);display:flex;align-items:center;justify-content:center;font-size:15px;flex-shrink:0}
.conn-ip{font-family:IBM Plex Mono,ui-monospace,monospace;font-size:13px;font-weight:700;color:var(--t1)}
.conn-label{font-size:10.5px;color:var(--t3);margin-top:1px}
.conn-meta{display:flex;justify-content:space-between;align-items:center;font-size:10px;color:var(--t3);padding-top:10px;border-top:1px solid var(--card-b)}

/* ══════ لاگ فعالیت‌ها ══════ */
.log-timeline{display:flex;flex-direction:column}
.log-item{display:flex;gap:12px;padding:11px 0;border-bottom:1px solid rgba(111,156,240,.05);position:relative}
.log-item:last-child{border-bottom:none}
.log-ic{width:30px;height:30px;border-radius:9px;display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0}
.log-ic.ok{background:var(--green-bg);color:var(--green-t)}
.log-ic.err{background:var(--red-bg);color:var(--red-t)}
.log-ic.warn{background:var(--amber-bg);color:var(--amber-t)}
.log-ic.info{background:var(--accent-d);color:var(--accent2)}
.log-body{flex:1;min-width:0}
.log-msg{font-size:12.5px;color:var(--t1);line-height:1.6}
.log-time{font-size:9.5px;color:var(--t3);margin-top:2px;display:flex;align-items:center;gap:5px}
.log-kind{font-size:8.5px;padding:1px 7px;border-radius:10px;background:var(--accent-d);color:var(--accent2);font-weight:700;text-transform:uppercase;letter-spacing:.04em}
.erow{padding:9px 0;border-bottom:1px solid rgba(111,156,240,.05)}
.erow:last-child{border-bottom:none}
.etime{color:var(--t3);font-size:9.5px;margin-bottom:3px;display:flex;align-items:center;gap:4px}
.emsg{color:var(--red-t);font-family:IBM Plex Mono,ui-monospace,monospace;background:var(--red-bg);padding:6px 9px;border-radius:6px;word-break:break-all;font-size:10.5px}

@media(max-width:1050px){
  .sidebar{transform:translateX(-100%)}
  .sidebar.open{transform:translateX(0);box-shadow:10px 0 40px rgba(0,0,0,.4)}
  .sb-close{display:flex}
  .main{margin-left:0;padding-top:70px}
  .mob-top{display:flex}
  .metrics{grid-template-columns:1fr 1fr}
  .g2,.g3{grid-template-columns:1fr}
}
@media(max-width:500px){
  .metrics{grid-template-columns:1fr}
  .main{padding:62px 12px 50px}
  .sub-grid,.cfg-grid,.conn-grid{grid-template-columns:1fr}
}
.cfgdash-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px}
.cfgdash-item{background:var(--card);border:1px solid var(--card-b);border-radius:14px;padding:13px 14px;cursor:pointer;transition:.15s}
.cfgdash-item:hover{border-color:var(--card-bh)}
.cfgdash-item.on{border-color:var(--accent);box-shadow:0 0 0 1px var(--accent) inset}
.cfgdash-item-top{display:flex;align-items:center;gap:7px;margin-bottom:8px}
.cfgdash-item-label{font-size:12.5px;font-weight:700;color:var(--t1);flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.cfgdash-stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px;margin-bottom:14px}
.cfgdash-stat{background:var(--accent-d);border:1px solid var(--card-b);border-radius:12px;padding:12px 13px}
.cfgdash-stat-l{font-size:9px;color:var(--t3);font-weight:700;text-transform:uppercase;letter-spacing:.05em;margin-bottom:6px}
.cfgdash-stat-v{font-size:16px;font-weight:800;color:var(--t1)}
.cfgdash-ip-row{display:flex;align-items:center;gap:10px;padding:9px 11px;border-radius:10px;background:var(--accent-d);border:1px solid var(--card-b);margin-bottom:6px;flex-wrap:wrap}
.cfgdash-ip-row .ip{font-family:IBM Plex Mono,ui-monospace,monospace;font-size:12px;color:var(--t1);display:flex;align-items:center;gap:7px}
.cfgdash-ip-meta{display:flex;align-items:center;gap:12px;font-size:10.5px;color:var(--t3);margin-left:auto;flex-wrap:wrap}

/* ══════ Classic dark refinement ══════ */
body{font-family:'IBM Plex Sans',system-ui,sans-serif;line-height:1.5;-webkit-font-smoothing:antialiased}
.vl-code,.sub-url,.cfg-uuid-mini,.conn-ip-v2,.conn-ip,.sub-card-url-text,.cfgdash-ip-row .ip,.emsg{font-family:'IBM Plex Mono',ui-monospace,monospace}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.pg.on,.pulse,.conn-live-dot{animation:none}

/* sidebar */
.sidebar{background:var(--bg2);border-right:1px solid var(--card-b)}
.logo{padding:18px 18px 16px;gap:8px;align-items:baseline}
.logo-name{font-size:16px;font-weight:600;letter-spacing:0}
.logo-sub{font-size:11.5px;margin-top:0}
.nav-sec{font-size:11.5px;letter-spacing:0;text-transform:none;font-weight:600;color:var(--t3);padding:16px 18px 6px}
.nav-it{font-size:13.5px;border-left:none;border-radius:4px;margin:1px 8px;padding:8px 12px;gap:10px}
.nav-it:hover{background:var(--bg3);color:var(--t1)}
.nav-it.on{background:var(--bg3);color:var(--t1);box-shadow:inset 2px 0 0 var(--accent);font-weight:500}
.nav-badge{background:var(--bg3);color:var(--t2);border-radius:3px;font-size:11px;padding:1px 7px;font-weight:600}
.nav-it.on .nav-badge{background:var(--card)}
.theme-btn,.logout-btn,.menu-btn,.theme-mob,.sb-close{border-radius:4px;font-size:13px}
.theme-btn{background:transparent;border:1px solid var(--card-b);color:var(--t2)}
.theme-btn:hover{background:var(--bg3);color:var(--t1)}
.logout-btn{background:transparent;border:1px solid rgba(217,96,90,.35);color:var(--red-t)}
.logout-btn:hover{background:var(--red-bg)}
.menu-btn,.theme-mob,.sb-close{background:transparent;border:1px solid var(--card-b);color:var(--t2)}
.mob-top{background:var(--bg2)}
.mob-title{font-size:15px;font-weight:600}
.overlay,.modal-bg{backdrop-filter:none;background:rgba(0,0,0,.62)}

/* page header */
.main{padding:28px 32px 60px}
.tb-title{font-size:20px;font-weight:600;letter-spacing:0}
.tb-title i{color:var(--t3);font-size:20px}
.tb-sub{font-size:12.5px}

/* surfaces */
.metric,.card,.traf-main-stat,.traf-mini,.traf-chart-card,.vless-box,.create-panel,.srv-panel,.pw-panel,.conn-hero-tile,.conn-card-v2,.conn-card,.sub-card,.cfg-card,.bulk-bar,.cfgdash-item,.modal,.modal-v2,.conn-empty-v2,.subs-empty-v2,.toast{background:var(--card);background-image:none;border:1px solid var(--card-b);border-radius:6px;box-shadow:none}
.metric:hover,.card:hover,.traf-mini:hover,.conn-hero-tile:hover,.conn-card-v2:hover,.conn-card:hover,.sub-card:hover,.cfg-card:hover,.cfgdash-item:hover{border-color:var(--card-bh);transform:none;box-shadow:none}
.cfgdash-item.on{border-color:var(--accent);box-shadow:none;background:var(--accent-d)}
.metric::after,.traf-main-stat::before,.vless-box::before,.create-panel::before,.srv-panel::before,.pw-panel::before,.sub-card-top::before,.modal-v2-head::before,.conn-card-v2-glow,.conn-hero-tile::after,.conn-avatar::after,.conn-duration-fill::after,.conn-card::before{display:none}
.sub-card-top,.modal-v2-head,.lmodal-head{background:none;border-bottom:1px solid var(--card-b)}
.conn-card-v2-divider{background:var(--card-b)}
.metric{padding:16px 18px}
.card{padding:18px 20px}
.card-title{font-size:14px;font-weight:600}
.card-title i{color:var(--t3)}
.cp-block,.srv-tile,.sub-card-stats,.cfgdash-stat,.cfgdash-ip-row,.sub-card-url-row,.sub-box,.cl,.modal-v2-hint,.vl-code,.proto-card{background:var(--bg3);border:1px solid var(--card-b);border-radius:4px;box-shadow:none}
.proto-card:hover{border-color:var(--card-bh);transform:none}
.proto-card.active{border-color:var(--accent);background:var(--accent-d);box-shadow:none}
.proto-card-check{border-radius:3px;background:var(--accent-s)}
.cl.amber{background:var(--amber-bg);border-color:rgba(201,154,60,.3)}
.sub-url,.sub-card-url-text,.vl-code,.cfg-uuid-mini{color:var(--accent2)}
.sub-card-url-row{border-style:solid}
.sub-card-url-copy{color:var(--t2)}
.conn-empty-v2,.subs-empty-v2{border-style:solid}

/* icon tiles */
.m-icon,.cp-head-icon,.srv-hero-icon,.pw-hero-icon,.conn-avatar,.sub-card-icon,.modal-v2-icon,.lmodal-icon,.traf-mini-icon,.conn-hero-icon,.srv-tile-icon,.proto-card-icon,.lrow-v2-avatar,.conn-stat-icon,.log-ic,.conn-ip-icon,.conn-empty-v2-icon,.subs-empty-v2-icon{border-radius:4px;background:var(--bg3);color:var(--accent);box-shadow:none;border:1px solid var(--card-b)}
.proto-card.active .proto-card-icon,.lrow-v2.checked .lrow-v2-avatar{background:var(--accent-s);border-color:var(--accent-s);color:#fff}

/* text hierarchy: sentence case, readable sizes */
.m-label,.traf-main-label,.traf-mini-label,.fg label,.cp-block-label,.srv-tile-label,.pw-field label,.conn-hero-label,.conn-stat-text-label,.sub-card-stat-label,.modal-v2-field label,.cfgdash-stat-l,.vl-title,.conn-toolbar-title{font-size:12px;text-transform:none;letter-spacing:0;font-weight:500;color:var(--t2)}
.m-val,.traf-main-val,.traf-mini-val,.conn-hero-val,.cfgdash-stat-v,.sub-card-stat-val{font-weight:600;letter-spacing:0}
.cp-head-title,.srv-hero-domain,.pw-hero-title,.sub-card-name-v2,.modal-v2-title,.lmodal-title-v2,.traf-chart-title,.cfg-label,.conn-empty-v2-title,.subs-empty-v2-title,.conn-ip-v2,.lrow-v2-name,.cfgdash-item-label{font-weight:600;letter-spacing:0}
.m-sub,.utxt,.cfg-sub-meta,.df-text,.conn-label,.conn-label-v2,.cp-head-sub,.srv-hero-sub,.pw-hero-sub,.traf-chart-sub,.traf-mini-sub,.cfg-sub-tag,.lrow-v2-meta,.etime,.log-time,.modal-v2-sub,.lmodal-sub-v2,.conn-empty-v2-sub,.subs-empty-v2-sub,.sub-card-desc-v2,.conn-meta{font-size:11.5px}
.sr{font-size:13px;border-bottom-color:var(--card-b)}
.sr-v{font-size:13px}
.log-item,.erow,.lrow{border-bottom-color:var(--card-b)}
.log-msg{font-size:13px}
.log-kind{border-radius:3px;text-transform:none;letter-spacing:0;font-size:11px;font-weight:500;background:var(--bg3);color:var(--t2)}
.emsg{border-radius:4px;font-size:11.5px}

/* status pills */
.badge,.exp-chip,.proto-chip,.conn-status-pill,.conn-live-badge,.lrow-v2-status,.traf-trend,.lrow-badge{border-radius:3px;font-size:11px;font-weight:600;padding:2px 8px}
.conn-live-badge{border:1px solid rgba(63,167,122,.3)}
.pc-xhttp,.bg-purple{background:var(--purple-bg);color:var(--t2)}

/* buttons */
.btn{border-radius:4px;font-weight:500;font-size:13px;padding:8px 14px;transition:background .12s,border-color .12s}
.btn-sm{font-size:12px;padding:5px 10px}
.btn-icon{border-radius:4px}
.btn-p,.cp-submit-btn,.pw-submit,.modal-v2-btn-submit{background:var(--accent-s);color:#fff;border:1px solid transparent;border-radius:4px;box-shadow:none;font-weight:600}
.btn-p:hover,.cp-submit-btn:hover,.pw-submit:hover,.modal-v2-btn-submit:hover{background:#4a7fe6;transform:none;box-shadow:none}
.cp-submit-btn,.pw-submit,.modal-v2-btn-submit{font-size:13px;padding:10px 20px}
.cp-submit-btn:active,.pw-submit:active,.modal-v2-btn-submit:active{transform:none}
.btn-o,.modal-v2-btn-cancel{background:transparent;border:1px solid var(--card-b);color:var(--t2);border-radius:4px}
.btn-o:hover,.modal-v2-btn-cancel:hover{background:var(--bg3);border-color:var(--card-bh);color:var(--t1)}
.btn-g,.btn-pur{background:var(--bg3);color:var(--t1);border:1px solid var(--card-b)}
.btn-g:hover,.btn-pur:hover{border-color:var(--card-bh);background:var(--bg3)}
.btn-d{background:transparent;color:var(--red-t);border:1px solid rgba(217,96,90,.35)}
.btn-d:hover{background:var(--red-bg)}
.btn-amber{background:transparent;color:var(--amber-t);border:1px solid rgba(201,154,60,.35)}
.btn-amber:hover{background:var(--amber-bg)}
.modal-close,.modal-v2-close{border-radius:4px;background:transparent}
.chip{border-radius:4px;font-size:12px;font-weight:500;background:var(--bg3);color:var(--t2)}
.chip:hover{background:var(--bg3);color:var(--t1);border-color:var(--card-bh)}
.chip.active{background:var(--accent-s);border-color:var(--accent-s);color:#fff;box-shadow:none}
.traf-range-tabs{border-radius:5px;background:var(--bg3)}
.traf-range-tab{border-radius:3px;font-size:12px;font-weight:500}
.traf-range-tab.on{background:var(--accent-s);box-shadow:none}

/* inputs */
.fi,.fs,.cp-input-full,.pw-input,.modal-v2-input,.lmodal-search input,.subs-search input{background:var(--input);border:1px solid var(--card-b);border-radius:4px;font-size:13px;color:var(--t1);box-shadow:none}
.fi:focus,.fs:focus,.cp-input-full:focus,.pw-input:focus,.modal-v2-input:focus,.lmodal-search input:focus,.subs-search input:focus{border-color:var(--accent);box-shadow:0 0 0 2px var(--accent-d);background:var(--input)}
.lmodal-qbtn{border-radius:4px;background:var(--bg3);color:var(--t2)}
.lrow-v2{border-radius:4px}
.lrow-v2.checked{background:var(--accent-d);border-color:var(--accent)}
.lrow-v2-check{border-radius:3px}
.lrow-v2.checked .lrow-v2-check{background:var(--accent-s);border-color:var(--accent-s)}

/* bars & toggles */
.spbar,.ubar,.pw-strength,.conn-duration-track{border-radius:2px;background:var(--bg3)}
.spfill,.ubar-f,.conn-duration-fill{border-radius:2px;background:var(--accent)}
.conn-duration-fill{background:var(--green)}
.pw-strength-seg{border-radius:2px}
.pw-req{border-radius:3px}

/* cards in lists */
.cfg-card{border-radius:6px}
.cfg-status-dot{box-shadow:none}
.toast{font-size:13px}

@media(max-width:1050px){.main{padding:70px 16px 50px}}
@media(max-width:500px){.main{padding:62px 12px 50px}}
</style>
</head>
<body>
<div class="toast" id="toast"></div>
<div class="modal-bg" id="modal-edit-link">
  <div class="modal">
    <button class="modal-close" onclick="closeModal('modal-edit-link')"><i class="ti ti-x"></i></button>
    <div class="modal-title"><i class="ti ti-edit"></i> Edit config</div>
    <input type="hidden" id="el-uuid">
    <div class="fg" style="margin-bottom:13px"><label>Title</label><input class="fi" id="el-label" style="width:100%"></div>
    <div class="form-row" style="margin-bottom:13px">
      <div class="fg" style="flex:1"><label>Quota (0 = unlimited)</label><input class="fi" id="el-val" type="number" min="0" step="0.1" style="width:100%"></div>
      <div class="fg"><label>Unit</label><select class="fs" id="el-unit"><option value="GB">GB</option><option value="MB">MB</option></select></div>
    </div>
    <div class="fg" style="margin-bottom:13px"><label>Expiry (days from now, 0 = no change/unlimited)</label><input class="fi" id="el-exp" type="number" min="0" step="1" style="width:100%"></div>
    <div class="fg" style="margin-bottom:13px"><label>Note</label><input class="fi" id="el-note" style="width:100%"></div>
    <div class="form-row" style="margin-bottom:13px">
      <div class="fg" style="flex:1"><label>Fingerprint (uTLS)</label>
        <select class="fs" id="el-fp" style="width:100%">
          <option value="chrome">chrome</option>
          <option value="firefox">firefox</option>
          <option value="safari">safari</option>
          <option value="ios">ios</option>
          <option value="android">android</option>
          <option value="edge">edge</option>
          <option value="360">360</option>
          <option value="qq">qq</option>
          <option value="random">random</option>
          <option value="randomized">randomized</option>
        </select>
      </div>
      <div class="fg" style="flex:1"><label>ALPN (empty = default)</label><input class="fi" id="el-alpn" placeholder="e.g. h2,http/1.1" style="width:100%"></div>
    </div>
    <div class="form-row" style="margin-bottom:16px">
      <div class="fg" style="flex:1"><label>Connection port</label><input class="fi" id="el-port" type="number" min="1" max="65535" style="width:100%"></div>
      <div class="fg" style="flex:1"><label>IP limit (0 = unlimited)</label><input class="fi" id="el-iplimit" type="number" min="0" step="1" style="width:100%"></div>
    </div>
    <div class="form-row" style="margin-bottom:16px">
      <div class="fg" style="flex:1"><label>Speed limit (0 = unlimited)</label><input class="fi" id="el-speed" type="number" min="0" step="0.5" style="width:100%"></div>
      <div class="fg"><label>Unit</label><select class="fs" id="el-speed-unit"><option value="MBIT">Mbps</option><option value="KB">KB/s</option><option value="MB">MB/s</option></select></div>
    </div>
    <div class="cl"><i class="ti ti-info-circle"></i><span>To keep the current expiry, leave the expiry field at 0.</span></div>
    <div style="margin-top:16px;display:flex;gap:8px;justify-content:flex-end">
      <button class="btn btn-o" onclick="closeModal('modal-edit-link')">Cancel</button>
      <button class="btn btn-p" onclick="saveEditLink()"><i class="ti ti-check"></i> Save changes</button>
    </div>
  </div>
</div>
<div class="modal-bg" id="modal-link-chart">
  <div class="modal" style="max-width:640px">
    <button class="modal-close" onclick="closeModal('modal-link-chart')"><i class="ti ti-x"></i></button>
    <div class="modal-title" id="lc-title"><i class="ti ti-chart-line"></i> Usage chart</div>
    <div style="height:280px;margin-top:10px"><canvas id="lc-canvas"></canvas></div>
  </div>
</div>
<div class="mob-top">
  <div class="ml">
    <span class="mob-title">Panel</span>
  </div>
  <div class="mob-right">
    <button class="theme-mob" id="theme-mob-btn" onclick="toggleTheme()"><i class="ti ti-sun" id="theme-mob-icon"></i></button>
    <button class="menu-btn" id="open-sb"><i class="ti ti-menu-2"></i></button>
  </div>
</div>
<div class="overlay" id="overlay"></div>
<aside class="sidebar" id="sb">
  <button class="sb-close" id="close-sb"><i class="ti ti-x"></i></button>
  <div class="logo"><span class="logo-name">Panel</span><span class="logo-sub">v9.8</span></div>
  <div class="nav-wrap">
    <div class="nav-sec">Panel</div>
    <div class="nav-it on" data-pg="overview"><i class="ti ti-layout-dashboard"></i> Dashboard</div>
    <div class="nav-it" data-pg="links"><i class="ti ti-link-plus"></i> Configs <span class="nav-badge" id="links-nb">0</span></div>
    <div class="nav-it" data-pg="cfgdash"><i class="ti ti-chart-infographic"></i> Config dashboard</div>
    <div class="nav-it" data-pg="traffic"><i class="ti ti-chart-area"></i> Traffic</div>
    <div class="nav-it" data-pg="connections"><i class="ti ti-plug-connected"></i> Connections <span class="nav-badge" id="conns-nb">0</span></div>
    <div class="nav-sec">System</div>
    <div class="nav-it" data-pg="security"><i class="ti ti-shield-lock"></i> Security</div>
    <div class="nav-it" data-pg="logs"><i class="ti ti-history"></i> Activity log</div>
    <div class="nav-it" data-pg="errors"><i class="ti ti-alert-triangle"></i> Errors</div>
    <div class="nav-it" data-pg="testws"><i class="ti ti-wifi"></i> WebSocket test</div>
    <div class="nav-it" data-pg="settings"><i class="ti ti-settings"></i> Settings</div>
      </div>
  <div class="sb-foot">
    <button class="theme-btn" onclick="toggleTheme()"><i class="ti ti-moon" id="theme-icon"></i> <span id="theme-label">Light theme</span></button>
    
    <button class="logout-btn" id="logout-btn"><i class="ti ti-logout"></i> Logout</button>
  </div>
</aside>
<main class="main">
<section class="pg on" id="pg-overview">
  <div class="topbar">
    <div><div class="tb-title"><i class="ti ti-layout-dashboard"></i> Dashboard</div><div class="tb-sub" id="last-upd">Loading...</div></div>
    <div class="tb-right">
      <span class="badge bg-green"><span class="dot dg pulse"></span> Active</span>
      <span class="badge bg-blue" id="uptime-badge">—</span>
      <button class="btn btn-p btn-sm" onclick="refreshAll()"><i class="ti ti-refresh"></i> Refresh</button>
    </div>
  </div>
  <div class="metrics">
    <div class="metric"><div class="m-icon"><i class="ti ti-plug-connected"></i></div><div class="m-label">Active connections</div><div class="m-val" id="m-conns">—</div><div class="m-sub"><span class="dot dg pulse"></span> Live WebSocket / XHTTP</div></div>
    <div class="metric"><div class="m-icon"><i class="ti ti-transfer"></i></div><div class="m-label">Total traffic</div><div class="m-val" id="m-traffic">—<span class="m-unit">MB</span></div><div class="m-sub">Since startup</div></div>
    <div class="metric suc"><div class="m-icon suc"><i class="ti ti-link"></i></div><div class="m-label">Active configs</div><div class="m-val" id="m-alinks">—</div><div class="m-sub" id="m-lsub">of total</div></div>
    <div class="metric dan" style="cursor:pointer" onclick="navTo('errors')" title="View error details"><div class="m-icon dan"><i class="ti ti-alert-triangle"></i></div><div class="m-label">Errors</div><div class="m-val" id="m-errs">—</div><div class="m-sub">Since startup</div></div>
  </div>
  <div class="g3">
    <div class="card"><div class="card-title"><i class="ti ti-chart-area"></i> Hourly traffic (MB)</div><div class="ch"><canvas id="ch1"></canvas></div></div>
    <div class="card"><div class="card-title"><i class="ti ti-chart-donut"></i> Distribution</div><div class="ch-sm"><canvas id="ch2"></canvas></div></div>
  </div>
  <div class="g2">
    <div class="card">
      <div class="card-title"><i class="ti ti-activity"></i> Service status</div>
      <div class="sr"><span class="sr-k"><i class="ti ti-shield-check"></i> UUID Auth</span><span class="sr-v" style="color:var(--green-t)">● Active · strict</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-circle-check"></i> VLESS / WS Tunnel</span><span class="sr-v" style="color:var(--green-t)">● Active</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-bolt"></i> Siz10a XHTTP Ultra</span><span class="sr-v" style="color:var(--green-t)">● Active · mode: auto</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-rss"></i> Subscription API</span><span class="sr-v" style="color:var(--green-t)">● Active</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-clock"></i> Uptime</span><span class="sr-v" id="uptime-inline">—</span></div>
      <div class="sr" style="flex-direction:column;align-items:flex-start;gap:4px">
        <div style="width:100%;display:flex;justify-content:space-between"><span class="sr-k"><i class="ti ti-gauge"></i> Relative load</span><span class="sr-v" id="bw-pct">—%</span></div>
        <div class="spbar" style="width:100%"><div class="spfill" id="bw-bar" style="width:0%"></div></div>
      </div>
    </div>
    <div class="card">
      <div class="card-title"><i class="ti ti-list"></i> Config summary <span class="ml-auto badge bg-blue" id="lsummary-badge">0</span></div>
      <div id="lsummary">—</div>
    </div>
  </div>
  <div class="dash-footer">
    <span class="df-text">Panel v9.8 · Railway</span>
    
  </div>
</section>
<section class="pg" id="pg-links">
  <div class="topbar">
    <div><div class="tb-title"><i class="ti ti-link-plus"></i> Configs</div><div class="tb-sub">Create and manage configs with quotas and expiry</div></div>
    <div class="tb-right"><span class="badge bg-blue" id="links-pg-cnt">0 configs</span></div>
  </div>
  <div class="create-panel">
    <div class="cp-head">
      <div class="cp-head-icon"><i class="ti ti-square-rounded-plus"></i></div>
      <div class="cp-head-text">
        <div class="cp-head-title">Create new config</div>
        <div class="cp-head-sub">Random UUID · choose quota, expiry and protocol</div>
      </div>
    </div>
    <div class="cp-body">
      <div class="cp-row">
        <div class="cp-block">
          <div class="cp-block-label"><i class="ti ti-id-badge-2"></i> Config identifier</div>
          <input class="cp-input-full" id="nl-label" placeholder="e.g. User Ali">
          <div class="cp-mini-row">
            <input class="cp-input-full" id="nl-note" placeholder="Note (optional)">
          </div>
        </div>
        <div class="cp-block">
          <div class="cp-block-label"><i class="ti ti-calendar-due"></i> Expiry</div>
          <div class="cp-mini-row">
            <input class="cp-input-full" id="nl-exp" type="number" min="0" step="1" placeholder="Expiry (days) · 0 = unlimited">
          </div>
          <div class="chip-row" id="exp-chips">
            <span class="chip" onclick="setExpiry(0,this)">Unlimited</span>
            <span class="chip" onclick="setExpiry(7,this)">7 days</span>
            <span class="chip active" onclick="setExpiry(30,this)">30 days</span>
            <span class="chip" onclick="setExpiry(90,this)">90 days</span>
          </div>
        </div>
      </div>
      <div class="cp-block mb16">
        <div class="cp-block-label"><i class="ti ti-gauge"></i> Traffic quota</div>
        <div class="cp-quota-inputs">
          <input class="cp-input-full" id="nl-val" type="number" min="0" step="0.1" placeholder="0 = unlimited">
          <select class="cp-input-full fs" id="nl-unit"><option value="GB">GB</option><option value="MB" selected>MB</option></select>
        </div>
        <div class="chip-row" id="quota-chips">
          <span class="chip" onclick="setQuota(0,'GB',this)">Unlimited</span>
          <span class="chip" onclick="setQuota(500,'MB',this)">500 MB</span>
          <span class="chip active" onclick="setQuota(1,'GB',this)">1 GB</span>
          <span class="chip" onclick="setQuota(5,'GB',this)">5 GB</span>
          <span class="chip" onclick="setQuota(10,'GB',this)">10 GB</span>
          <span class="chip" onclick="setQuota(50,'GB',this)">50 GB</span>
        </div>
      </div>
      <div class="cp-block mb16">
        <div class="cp-block-label"><i class="ti ti-plug-connected"></i> Transport protocol</div>
        <select id="nl-proto" style="display:none">
          <option value="vless-ws">VLESS / WebSocket</option>
          <option value="xhttp">XHTTP Ultra · mode: auto</option>
        </select>
        <div class="proto-cards" style="grid-template-columns:repeat(2,1fr)">
          <div class="proto-card active" data-val="vless-ws" onclick="selectProto('vless-ws',this)">
            <div class="proto-card-check"><i class="ti ti-check"></i></div>
            <div class="proto-card-icon"><i class="ti ti-link"></i></div>
            <div class="proto-card-title">VLESS / WS</div>
            <div class="proto-card-desc">Stable and general-purpose</div>
          </div>
          <div class="proto-card" data-val="xhttp" onclick="selectProto('xhttp',this)">
            <div class="proto-card-check"><i class="ti ti-check"></i></div>
            <div class="proto-card-icon"><i class="ti ti-bolt"></i></div>
            <div class="proto-card-title">XHTTP · mode: auto</div>
            <div class="proto-card-desc">Auto-selects packet-up/stream-up</div>
          </div>
        </div>
      </div>
      <div class="cp-row">
        <div class="cp-block">
          <div class="cp-block-label"><i class="ti ti-fingerprint"></i> Fingerprint (uTLS)</div>
          <select class="cp-input-full fs" id="nl-fp">
            <option value="chrome" selected>chrome</option>
            <option value="firefox">firefox</option>
            <option value="safari">safari</option>
            <option value="ios">ios</option>
            <option value="android">android</option>
            <option value="edge">edge</option>
            <option value="360">360</option>
            <option value="qq">qq</option>
            <option value="random">random</option>
            <option value="randomized">randomized</option>
          </select>
        </div>
        <div class="cp-block">
          <div class="cp-block-label"><i class="ti ti-antenna-bars-5"></i> ALPN</div>
          <select class="cp-input-full fs" id="nl-alpn-preset" onchange="onAlpnPresetChange()">
            <option value="">Protocol default</option>
            <option value="h2,http/1.1">h2,http/1.1</option>
            <option value="http/1.1">http/1.1</option>
            <option value="h2">h2</option>
            <option value="__custom__">Custom...</option>
          </select>
          <div class="cp-mini-row">
            <input class="cp-input-full" id="nl-alpn" placeholder="Custom ALPN value" style="display:none">
          </div>
        </div>
      </div>
      <div class="cp-row mb16" style="grid-template-columns:1fr">
        <div class="cp-block">
          <div class="cp-block-label"><i class="ti ti-users"></i> IP limit / concurrent users</div>
          <input class="cp-input-full" id="nl-iplimit" type="number" min="0" step="1" placeholder="0 = unlimited" value="0">
          <div class="chip-row" id="iplimit-chips">
            <span class="chip active" onclick="setIpLimit(0,this)">Unlimited</span>
            <span class="chip" onclick="setIpLimit(1,this)">1 user</span>
            <span class="chip" onclick="setIpLimit(2,this)">2 users</span>
            <span class="chip" onclick="setIpLimit(5,this)">5 users</span>
          </div>
        </div>
      </div>
      <div class="cp-row mb16">
        <div class="cp-block" style="flex:1">
          <div class="cp-block-label"><i class="ti ti-gauge"></i> Speed limit</div>
          <div class="form-row">
            <input class="cp-input-full" id="nl-speed" type="number" min="0" step="0.5" placeholder="0 = unlimited" value="0" style="flex:1">
            <select class="fs" id="nl-speed-unit" style="flex:0 0 100px">
              <option value="MBIT" selected>Mbps</option>
              <option value="KB">KB/s</option>
              <option value="MB">MB/s</option>
            </select>
          </div>
          <div class="chip-row" id="speed-chips">
            <span class="chip active" onclick="setSpeedLimit(0,this)">Unlimited</span>
            <span class="chip" onclick="setSpeedLimit(1,this)">1 Mbps</span>
            <span class="chip" onclick="setSpeedLimit(5,this)">5 Mbps</span>
            <span class="chip" onclick="setSpeedLimit(10,this)">10 Mbps</span>
            <span class="chip" onclick="setSpeedLimit(25,this)">25 Mbps</span>
          </div>
        </div>
      </div>
      <div class="cp-footer">
        <div class="cp-footer-note"><i class="ti ti-info-circle"></i> UUID is fully random · only registered UUIDs may connect · the protocol can't be changed after creation.</div>
        <button class="cp-submit-btn" onclick="createLink()"><i class="ti ti-link-plus"></i> Create config</button>
      </div>
    </div>
  </div>
  <div class="links-toolbar">
    <div class="subs-search">
      <i class="ti ti-search"></i>
      <input id="links-search" placeholder="Search by name, note or UUID..." oninput="renderLinksGrid()">
    </div>
    <select id="links-sort" class="fs" style="min-width:180px" onchange="renderLinksGrid()">
      <option value="newest">Sort: newest</option>
      <option value="name">Name (A–Z)</option>
      <option value="usage_desc">Highest usage</option>
      <option value="usage_asc">Lowest usage</option>
      <option value="remaining_asc">Least remaining quota</option>
      <option value="active_first">Active first</option>
    </select>
    <label class="bulk-selall">
      <input type="checkbox" id="links-selall" onchange="toggleSelectAllLinks(this)">
      <span>Select all</span>
    </label>
  </div>
  <div class="bulk-bar" id="links-bulkbar" style="display:none">
    <span class="bulk-count"><i class="ti ti-checkbox"></i> <span id="links-selcount">0</span> configs selected</span>
    <div class="bulk-actions">
      <button class="btn btn-sm btn-g" onclick="bulkLinksAction('activate')"><i class="ti ti-circle-check"></i> Activate</button>
      <button class="btn btn-sm btn-g" onclick="bulkLinksAction('deactivate')"><i class="ti ti-circle-x"></i> Deactivate</button>
      <button class="btn btn-sm btn-g" onclick="bulkLinksAction('reset')"><i class="ti ti-rotate"></i> Reset usage</button>
      <button class="btn btn-sm btn-d" onclick="bulkLinksAction('delete')"><i class="ti ti-trash"></i> Delete</button>
      <button class="btn btn-sm btn-o" onclick="clearLinksSelection()"><i class="ti ti-x"></i> Clear selection</button>
    </div>
  </div>
  <div class="cfg-grid" id="links-grid"></div>
  <div class="empty" id="links-empty" style="display:none"><i class="ti ti-link-off"></i><p>No configs yet</p></div>
  <div class="empty" id="links-empty-search" style="display:none"><i class="ti ti-search-off"></i><p>No results match your search</p></div>
</section>
<section class="pg" id="pg-cfgdash">
  <div class="topbar">
    <div><div class="tb-title"><i class="ti ti-chart-infographic"></i> Config dashboard</div><div class="tb-sub">Per-config analytics — status, usage and connected IPs</div></div>
    <div class="tb-right"><button class="btn btn-p btn-sm" onclick="loadCfgDash()"><i class="ti ti-refresh"></i> Refresh</button></div>
  </div>
  <div class="card" style="margin-bottom:16px">
    <div class="card-title"><i class="ti ti-list"></i> Select a config <span class="ml-auto badge bg-blue" id="cfgdash-count">0</span></div>
    <div class="cfgdash-grid" id="cfgdash-list"></div>
    <div class="empty" id="cfgdash-empty" style="display:none"><i class="ti ti-link-off"></i><p>No configs yet</p></div>
  </div>
  <div id="cfgdash-detail">
    <div class="card"><div class="empty"><i class="ti ti-hand-click"></i><p>Select a config from the list above to see its full analytics</p></div></div>
  </div>
</section>
<section class="pg" id="pg-traffic">
  <div class="topbar">
    <div><div class="tb-title"><i class="ti ti-chart-area"></i> Traffic</div><div class="tb-sub">Bandwidth usage analysis and monitoring</div></div>
    <div class="tb-right"><button class="btn btn-p btn-sm" onclick="refreshAll()"><i class="ti ti-refresh"></i> Refresh</button></div>
  </div>

  <div class="traf-hero">
    <div class="traf-main-stat">
      <div class="traf-main-label"><i class="ti ti-database"></i> Total traffic used</div>
      <div class="traf-main-val" id="t-traffic">—<span>MB</span></div>
      <div class="traf-trend up" id="t-trend"><i class="ti ti-trending-up"></i> <span id="t-trend-val">—</span></div>
    </div>
    <div class="traf-mini">
      <div class="traf-mini-top"><div class="traf-mini-icon"><i class="ti ti-arrow-up-right"></i></div><span class="traf-mini-label">Hourly average</span></div>
      <div><div class="traf-mini-val" id="t-avg">—</div><div class="traf-mini-sub">MB per hour</div></div>
    </div>
    <div class="traf-mini">
      <div class="traf-mini-top"><div class="traf-mini-icon pk"><i class="ti ti-chart-bar"></i></div><span class="traf-mini-label">Peak usage</span></div>
      <div><div class="traf-mini-val" id="t-peak">—</div><div class="traf-mini-sub" id="t-peak-time">Busiest hour</div></div>
    </div>
    <div class="traf-mini">
      <div class="traf-mini-top"><div class="traf-mini-icon lo"><i class="ti ti-clock-hour-4"></i></div><span class="traf-mini-label">Lowest usage</span></div>
      <div><div class="traf-mini-val" id="t-low">—</div><div class="traf-mini-sub">MB per hour</div></div>
    </div>
  </div>

  <div class="traf-chart-card">
    <div class="traf-chart-head">
      <div>
        <div class="traf-chart-title"><i class="ti ti-activity"></i> Traffic usage trend</div>
        <div class="traf-chart-sub">Megabytes per hour</div>
      </div>
      <div class="traf-legend">
        <div class="traf-legend-item"><span class="traf-legend-dot" style="background:var(--accent)"></span> Usage</div>
        <div class="traf-legend-item"><span class="traf-legend-dot" style="background:var(--amber)"></span> Average</div>
      </div>
    </div>
    <div class="traf-chart-body"><canvas id="ch3"></canvas></div>
  </div>
</section>
<section class="pg" id="pg-connections">
  <div class="topbar">
    <div><div class="tb-title"><i class="ti ti-plug-connected"></i> Active connections</div><div class="tb-sub">Live monitoring of IPs and traffic for each connection</div></div>
    <div class="tb-right"><span class="badge bg-green" id="conns-live">—</span><button class="btn btn-p btn-sm" onclick="refreshAll()"><i class="ti ti-refresh"></i> Refresh</button></div>
  </div>

  <div class="conn-hero">
    <div class="conn-hero-tile">
      <div class="conn-hero-icon"><i class="ti ti-plug-connected"></i></div>
      <div class="conn-hero-label">Live connections</div>
      <div class="conn-hero-val" id="ch-count">—</div>
    </div>
    <div class="conn-hero-tile">
      <div class="conn-hero-icon"><i class="ti ti-transfer"></i></div>
      <div class="conn-hero-label">Current total traffic</div>
      <div class="conn-hero-val" id="ch-traffic">—</div>
    </div>
    <div class="conn-hero-tile">
      <div class="conn-hero-icon"><i class="ti ti-clock"></i></div>
      <div class="conn-hero-label">Average connection duration</div>
      <div class="conn-hero-val" id="ch-avgdur">—</div>
    </div>
    <div class="conn-hero-tile">
      <div class="conn-hero-icon"><i class="ti ti-map-pin"></i></div>
      <div class="conn-hero-label">Unique IPs</div>
      <div class="conn-hero-val" id="ch-uniq">—</div>
    </div>
  </div>

  <div class="conn-toolbar">
    <div class="conn-toolbar-title"><i class="ti ti-list-details"></i> Connection list</div>
    <div class="conn-live-badge"><span class="conn-live-dot"></span> Auto-refresh every 5 seconds</div>
  </div>

  <div class="conn-grid-v2" id="conns-grid"></div>
  <div class="conn-empty-v2" id="conns-empty" style="display:none">
    <div class="conn-empty-v2-icon"><i class="ti ti-plug-off"></i></div>
    <div class="conn-empty-v2-title">No active connections</div>
    <div class="conn-empty-v2-sub">Clients will appear here as soon as they connect</div>
  </div>
</section>
<section class="pg" id="pg-security">
  <div class="topbar"><div><div class="tb-title"><i class="ti ti-shield-lock"></i> Security</div></div></div>
  <div class="g2">
    <div class="card">
      <div class="card-title"><i class="ti ti-lock"></i> Encryption</div>
      <div class="sr"><span class="sr-k"><i class="ti ti-certificate"></i> TLS/HTTPS</span><span class="sr-v" style="color:var(--green-t)">● Active (443)</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-fingerprint"></i> Fingerprint</span><span class="sr-v">Chrome Spoof</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-network"></i> Protocols</span><span class="sr-v">VLESS/WS + XHTTP Ultra</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-key"></i> Password hash</span><span class="sr-v">SHA-256+Salt</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-cookie"></i> Session</span><span class="sr-v">HttpOnly · 7 days</span></div>
    </div>
    <div class="card">
      <div class="card-title"><i class="ti ti-shield-check"></i> Access control</div>
      <div class="sr"><span class="sr-k"><i class="ti ti-id-badge"></i> Strict UUID auth</span><span class="sr-v" style="color:var(--green-t)">● Active v9</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-toggle-right"></i> Enable/disable config</span><span class="sr-v" style="color:var(--green-t)">● Active</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-gauge"></i> Traffic quota</span><span class="sr-v" style="color:var(--green-t)">● Active</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-calendar-x"></i> Expiry date</span><span class="sr-v" style="color:var(--green-t)">● Active</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-lock"></i> Public sub page password</span><span class="sr-v" style="color:var(--green-t)">● Optional · SHA-256</span></div>
    </div>
  </div>
</section>
<section class="pg" id="pg-logs">
  <div class="topbar"><div><div class="tb-title"><i class="ti ti-history"></i> Activity log</div><div class="tb-sub">Full history of panel events</div></div><div class="tb-right"><button class="btn btn-p btn-sm" onclick="loadActivity()"><i class="ti ti-refresh"></i></button></div></div>
  <div class="card"><div class="log-timeline" id="logs-list">—</div><div class="empty" id="logs-empty" style="display:none"><i class="ti ti-history-toggle"></i><p>No logs recorded yet</p></div></div>
</section>
<section class="pg" id="pg-errors">
  <div class="topbar"><div><div class="tb-title"><i class="ti ti-alert-triangle"></i> Errors</div></div><div class="tb-right"><span class="badge bg-red" id="errs-badge">0</span><button class="btn btn-p btn-sm" onclick="refreshAll()"><i class="ti ti-refresh"></i></button></div></div>
  <div class="card"><div class="card-title"><i class="ti ti-bug"></i> Error log</div><div id="errs-full">—</div></div>
</section>
<section class="pg" id="pg-testws">
  <div class="topbar"><div><div class="tb-title"><i class="ti ti-wifi"></i> WebSocket test</div></div></div>
  <div class="card" style="max-width:660px">
    <div class="cl amber" style="margin-top:0;margin-bottom:12px"><i class="ti ti-alert-triangle"></i><span>Only registered, active UUIDs can connect (this tests VLESS/WS only; XHTTP is tested from the client itself).</span></div>
    <div class="form-row" style="margin-bottom:12px">
      <div class="fg" style="flex:1"><label>UUID (must exist in Configs)</label><input class="fi" id="ws-uuid" placeholder="UUID of an active config" style="width:100%"></div>
      <button class="btn btn-p" onclick="wsConn()"><i class="ti ti-plug-connected"></i> Connect</button>
      <button class="btn btn-d" onclick="wsDisc()"><i class="ti ti-plug-x"></i> Disconnect</button>
    </div>
    <div class="form-row" style="margin-bottom:12px">
      <input class="fi" id="ws-msg" placeholder="Test message..." style="flex:1">
      <button class="btn btn-o" onclick="wsSend()"><i class="ti ti-send"></i> Send</button>
    </div>
    <div style="background:rgba(0,0,0,.3);border:1px solid var(--card-b);border-radius:10px;padding:14px;height:250px;overflow-y:auto;font-family:IBM Plex Mono,ui-monospace,monospace;font-size:10.5px;line-height:1.9" id="ws-log">
      <p style="color:var(--t3)">Waiting for connection...</p>
    </div>
  </div>
</section>
<section class="pg" id="pg-settings">
  <div class="topbar"><div><div class="tb-title"><i class="ti ti-settings"></i> Settings</div></div></div>
  <div class="g2">
    <div class="srv-panel">
      <div class="srv-hero">
        <div class="srv-hero-icon"><i class="ti ti-server-2"></i></div>
        <div class="srv-hero-text">
          <div class="srv-hero-domain" id="set-host">—</div>
          <div class="srv-hero-sub"><span class="dot dg pulse"></span> Online · Railway</div>
        </div>
      </div>
      <div class="srv-tiles">
        <div class="srv-tile"><div class="srv-tile-icon"><i class="ti ti-route"></i></div><div class="srv-tile-text"><div class="srv-tile-label">Default port</div><div class="srv-tile-val">443 (TLS) · changeable per config</div></div></div>
        <div class="srv-tile"><div class="srv-tile-icon"><i class="ti ti-versions"></i></div><div class="srv-tile-text"><div class="srv-tile-label">Version</div><div class="srv-tile-val">v9.8</div></div></div>
        <div class="srv-tile"><div class="srv-tile-icon"><i class="ti ti-brand-fastapi"></i></div><div class="srv-tile-text"><div class="srv-tile-label">Framework</div><div class="srv-tile-val">FastAPI + Uvicorn</div></div></div>
        <div class="srv-tile"><div class="srv-tile-icon"><i class="ti ti-cloud"></i></div><div class="srv-tile-text"><div class="srv-tile-label">Platform</div><div class="srv-tile-val">Railway</div></div></div>
        <div class="srv-tile" style="grid-column:1/-1"><div class="srv-tile-icon"><i class="ti ti-device-floppy"></i></div><div class="srv-tile-text"><div class="srv-tile-label">Storage</div><div class="srv-tile-val">JSON File (/data)</div></div></div>
      </div>
    </div>
    <div class="pw-panel">
      <div class="pw-hero">
        <div class="pw-hero-icon"><i class="ti ti-key"></i></div>
        <div class="pw-hero-text">
          <div class="pw-hero-title">Change password</div>
          <div class="pw-hero-sub">Choose a strong password and keep it somewhere safe</div>
        </div>
      </div>
      <div class="pw-body">
        <div class="pw-field">
          <label>Current password</label>
          <input class="pw-input" type="password" id="cp-cur" placeholder="Enter your current password">
          <button class="pw-eye" type="button" onclick="togglePwField('cp-cur',this)"><i class="ti ti-eye"></i></button>
        </div>
        <div class="pw-field" style="margin-bottom:6px">
          <label>New password</label>
          <input class="pw-input" type="password" id="cp-new" placeholder="At least 4 characters" oninput="checkPwStrength(this.value)">
          <button class="pw-eye" type="button" onclick="togglePwField('cp-new',this)"><i class="ti ti-eye"></i></button>
        </div>
        <div class="pw-strength" id="pw-strength-bar">
          <div class="pw-strength-seg"></div><div class="pw-strength-seg"></div><div class="pw-strength-seg"></div><div class="pw-strength-seg"></div>
        </div>
        <div class="pw-strength-label" id="pw-strength-label"><i class="ti ti-shield"></i> Password strength</div>
        <div class="pw-reqs">
          <span class="pw-req" id="req-len"><i class="ti ti-circle-dashed"></i> At least 4 characters</span>
          <span class="pw-req" id="req-num"><i class="ti ti-circle-dashed"></i> Contains a number</span>
          <span class="pw-req" id="req-case"><i class="ti ti-circle-dashed"></i> Upper/lowercase letters</span>
        </div>
        <div class="pw-field" style="margin-bottom:18px">
          <label>Confirm new password</label>
          <input class="pw-input" type="password" id="cp-cf" placeholder="Confirm new password">
          <button class="pw-eye" type="button" onclick="togglePwField('cp-cf',this)"><i class="ti ti-eye"></i></button>
        </div>
        <button class="pw-submit" onclick="changePw()"><i class="ti ti-shield-check"></i> Save new password</button>
      </div>
    </div>
  </div>
</section>
</main>
<script>
let isDark=localStorage.getItem('x4g-theme')!=='light';
function applyTheme(dark){
  document.documentElement.setAttribute('data-theme',dark?'dark':'light');
  const icon=dark?'ti-sun':'ti-moon',label=dark?'Light theme':'Dark theme';
  document.getElementById('theme-icon').className='ti '+icon;
  document.getElementById('theme-label').textContent=label;
  const mobI=document.getElementById('theme-mob-icon');if(mobI)mobI.className='ti '+icon;
}
function toggleTheme(){isDark=!isDark;localStorage.setItem('x4g-theme',isDark?'dark':'light');applyTheme(isDark)}
applyTheme(isDark);
function toast(msg,type=''){
  const t=document.getElementById('toast');
  t.textContent=msg;t.className='toast show'+(type?' '+type:'');
  setTimeout(()=>t.classList.remove('show'),2400);
}
function fmtB(b){if(!b||b===0)return '0 B';if(b<1024)return b+' B';if(b<1024**2)return (b/1024).toFixed(1)+' KB';if(b<1024**3)return (b/1024**2).toFixed(2)+' MB';return (b/1024**3).toFixed(2)+' GB'}
function fmtNum(n){return String(n)}
function esc(s){return String(s||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function daysLeft(exp){if(!exp)return null;return Math.ceil((new Date(exp)-Date.now())/(864e5))}
function expChip(exp,expired){
  if(expired)return '<span class="exp-chip ec-exp"><i class="ti ti-calendar-x"></i> Expired</span>';
  if(!exp)return '<span class="exp-chip ec-inf"><i class="ti ti-infinity"></i> Unlimited</span>';
  const d=daysLeft(exp);
  if(d<=0)return '<span class="exp-chip ec-exp"><i class="ti ti-calendar-x"></i> Expired</span>';
  if(d<=3)return `<span class="exp-chip ec-warn"><i class="ti ti-alert-triangle"></i> ${fmtNum(d)} days left</span>`;
  return `<span class="exp-chip ec-ok"><i class="ti ti-calendar-check"></i> ${fmtNum(d)} days left</span>`;
}
function protoBadge(p){
  const m={'vless-ws':['VLESS · WS','pc-ws'],'xhttp':['XHTTP · auto','pc-xhttp']};
  const v=m[p]||m['vless-ws'];
  return `<span class="proto-chip ${v[1]}">${v[0]}</span>`;
}
async function checkAuth(){try{const r=await fetch('/api/me');const d=await r.json();if(!d.authenticated)location.href='/login';}catch(e){location.href='/login'}}
async function logout(){try{await fetch('/api/logout',{method:'POST'})}catch(e){}location.href='/login'}
document.getElementById('logout-btn').addEventListener('click',logout);
async function authF(url,opts={}){
  const r=await fetch(url,opts);
  if(r.status===401){location.href='/login';throw new Error('unauthorized')}
  return r;
}
function setQuota(val,unit,el){
  document.getElementById('nl-val').value = val===0?'':val;
  document.getElementById('nl-unit').value = unit;
  document.querySelectorAll('#quota-chips .chip').forEach(c=>c.classList.remove('active'));
  el.classList.add('active');
}
function setExpiry(days,el){
  document.getElementById('nl-exp').value = days===0?'':days;
  document.querySelectorAll('#exp-chips .chip').forEach(c=>c.classList.remove('active'));
  el.classList.add('active');
}
function selectProto(val,el){
  document.getElementById('nl-proto').value = val;
  document.querySelectorAll('.proto-card').forEach(c=>c.classList.remove('active'));
  el.classList.add('active');
}
function setIpLimit(n,el){
  document.getElementById('nl-iplimit').value = n;
  document.querySelectorAll('#iplimit-chips .chip').forEach(c=>c.classList.remove('active'));
  el.classList.add('active');
}
function setSpeedLimit(n,el){
  document.getElementById('nl-speed').value = n;
  document.getElementById('nl-speed-unit').value = 'MBIT';
  document.querySelectorAll('#speed-chips .chip').forEach(c=>c.classList.remove('active'));
  el.classList.add('active');
}
function onAlpnPresetChange(){
  const p=document.getElementById('nl-alpn-preset').value;
  const inp=document.getElementById('nl-alpn');
  if(p==='__custom__'){inp.style.display='block';inp.value='';inp.focus();}
  else{inp.style.display='none';inp.value=p;}
}
const sb=document.getElementById('sb'),overlay=document.getElementById('overlay');
function openSb(){sb.classList.add('open');overlay.classList.add('show')}
function closeSb(){sb.classList.remove('open');overlay.classList.remove('show')}
document.getElementById('open-sb').addEventListener('click',openSb);
document.getElementById('close-sb').addEventListener('click',closeSb);
overlay.addEventListener('click',closeSb);
function navTo(name){
  document.querySelectorAll('.nav-it').forEach(n=>n.classList.toggle('on',n.dataset.pg===name));
  document.querySelectorAll('.pg').forEach(p=>p.classList.toggle('on',p.id==='pg-'+name));
  const loaders={links:loadLinks,connections:loadConns,errors:loadErrs,logs:loadActivity,cfgdash:loadCfgDash};
  if(loaders[name])loaders[name]();
  closeSb();window.scrollTo({top:0,behavior:'smooth'});
}
document.querySelectorAll('.nav-it').forEach(el=>el.addEventListener('click',()=>navTo(el.dataset.pg)));
function openModal(id){document.getElementById(id).classList.add('open')}
function closeModal(id){document.getElementById(id).classList.remove('open')}
let prevTraf=0,ch1,ch2,ch3;
async function fetchStats(){
  try{
    const r=await authF('/stats'),d=await r.json();
    document.getElementById('m-conns').textContent=d.active_connections;
    document.getElementById('conns-nb').textContent=d.active_connections;
    document.getElementById('m-traffic').innerHTML=d.total_traffic_mb.toFixed(1)+'<span class="m-unit">MB</span>';
    document.getElementById('m-alinks').textContent=d.active_links??'—';
    document.getElementById('m-lsub').textContent='of '+d.links_count+' configs';
    document.getElementById('m-errs').textContent=d.total_errors??'—';
    document.getElementById('errs-badge').textContent=d.total_errors+' errors';
    document.getElementById('uptime-inline').textContent=d.uptime;
    document.getElementById('uptime-badge').textContent='Railway · '+d.uptime;
    document.getElementById('last-upd').textContent='Last updated: '+new Date().toLocaleTimeString('en-US');
    document.getElementById('conns-live').innerHTML='<span class="dot dg pulse"></span> '+d.active_connections+' connections';
    document.getElementById('t-traffic').innerHTML=d.total_traffic_mb.toFixed(1)+'<span class="m-unit">MB</span>';
    const delta=d.total_traffic_mb-prevTraf,pct=Math.min(100,Math.round((delta/50)*100));
    document.getElementById('bw-pct').textContent=pct+'%';
    document.getElementById('bw-bar').style.width=pct+'%';
    prevTraf=d.total_traffic_mb;
    if(d.hourly){
      const labels=Object.keys(d.hourly).sort(),vals=labels.map(k=>+(d.hourly[k]/1024**2).toFixed(2));
      [ch1,ch3].forEach(c=>{if(!c)return;c.data.labels=labels;c.data.datasets[0].data=vals;c.update()});
      if(vals.length){const avg=vals.reduce((a,b)=>a+b,0)/vals.length,peak=Math.max(...vals);document.getElementById('t-avg').innerHTML=avg.toFixed(2)+'<span class="m-unit">MB</span>';document.getElementById('t-peak').innerHTML=peak.toFixed(2)+'<span class="m-unit">MB</span>';}
    }
    renderErrs(d.recent_errors||[]);
  }catch(e){console.error(e)}
}
function renderErrs(errs){
  const el=document.getElementById('errs-full');if(!el)return;
  if(!errs.length){el.innerHTML='<div style="color:var(--green-t);padding:10px;font-size:12px;display:flex;align-items:center;gap:5px"><i class="ti ti-circle-check"></i> No errors</div>';return}
  el.innerHTML=errs.slice().reverse().map(e=>`<div class="erow"><div class="etime"><i class="ti ti-clock"></i>${new Date(e.time).toLocaleString('en-US')}</div><div class="emsg">${esc(e.error)}${e.url?' — '+esc(e.url):''}</div></div>`).join('');
}
async function loadActivity(){
  try{
    const r=await authF('/api/activity'),d=await r.json();
    const logs=(d.logs||[]).slice().reverse();
    const el=document.getElementById('logs-list'),em=document.getElementById('logs-empty');
    if(!logs.length){el.innerHTML='';em.style.display='block';return}
    em.style.display='none';
    const icMap={ok:'ti-circle-check',err:'ti-circle-x',warn:'ti-alert-triangle',info:'ti-info-circle'};
    const kindFa={link:'Config',sub:'Group',auth:'Login',connection:'Connection',system:'System'};
    el.innerHTML=logs.map(l=>`
      <div class="log-item">
        <div class="log-ic ${l.level}"><i class="ti ${icMap[l.level]||'ti-info-circle'}"></i></div>
        <div class="log-body">
          <div class="log-msg">${esc(l.message)}</div>
          <div class="log-time"><i class="ti ti-clock"></i> ${new Date(l.time).toLocaleString('en-US')} <span class="log-kind">${kindFa[l.kind]||l.kind}</span></div>
        </div>
      </div>
    `).join('');
  }catch(e){console.error(e)}
}
let allLinksList=[];
let selectedLinks=new Set();
async function loadLinks(){
  try{
    const r=await authF('/api/links');
    const {links=[]}=await r.json();
    allLinksList=links;
    const validUuids=new Set(links.map(l=>l.uuid));
    selectedLinks.forEach(u=>{if(!validUuids.has(u))selectedLinks.delete(u)});
    document.getElementById('links-nb').textContent=links.length;
    document.getElementById('links-pg-cnt').textContent=fmtNum(links.length)+' configs';
    document.getElementById('lsummary-badge').textContent=fmtNum(links.length);
    document.getElementById('lsummary').innerHTML=links.length?links.slice(0,6).map(l=>`<div class="sr"><span class="sr-k" style="gap:5px"><i class="ti ${l.expired?'ti-calendar-x':l.active?'ti-circle-check':'ti-circle-x'}" style="color:${l.expired?'var(--amber)':l.active?'var(--green)':'var(--red)'}"></i>${esc(l.label)}</span><span class="sr-v" style="font-size:10px">${fmtB(l.used_bytes)} / ${l.limit_bytes===0?'∞':fmtB(l.limit_bytes)}</span></div>`).join(''):'<div class="empty"><i class="ti ti-link-off"></i><p>No configs</p></div>';
    renderLinksGrid();
  }catch(e){console.error(e)}
}
function filteredLinksList(){
  const q=(document.getElementById('links-search')?.value||'').trim().toLowerCase();
  let list=!q?allLinksList:allLinksList.filter(l=>
    (l.label||'').toLowerCase().includes(q) ||
    (l.note||'').toLowerCase().includes(q) ||
    (l.uuid||'').toLowerCase().includes(q)
  );
  const sortBy=document.getElementById('links-sort')?.value||'newest';
  const remaining=l=>l.limit_bytes===0?Infinity:Math.max(0,l.limit_bytes-l.used_bytes);
  list=list.slice();
  if(sortBy==='name'){
    list.sort((a,b)=>(a.label||'').localeCompare(b.label||'','fa'));
  }else if(sortBy==='usage_desc'){
    list.sort((a,b)=>(b.used_bytes||0)-(a.used_bytes||0));
  }else if(sortBy==='usage_asc'){
    list.sort((a,b)=>(a.used_bytes||0)-(b.used_bytes||0));
  }else if(sortBy==='remaining_asc'){
    list.sort((a,b)=>remaining(a)-remaining(b));
  }else if(sortBy==='active_first'){
    list.sort((a,b)=>((b.active&&!b.expired)?1:0)-((a.active&&!a.expired)?1:0));
  }else{
    list.sort((a,b)=>(b.created_at||'').localeCompare(a.created_at||''));
  }
  return list;
}
function renderLinksGrid(){
  const links=filteredLinksList();
  const grid=document.getElementById('links-grid'),empty=document.getElementById('links-empty'),emptySearch=document.getElementById('links-empty-search');
  if(!allLinksList.length){grid.innerHTML='';empty.style.display='block';emptySearch.style.display='none';updateBulkBar();return}
  if(!links.length){grid.innerHTML='';empty.style.display='none';emptySearch.style.display='block';updateBulkBar();return}
  empty.style.display='none';emptySearch.style.display='none';
  grid.innerHTML=links.map(l=>{
  const lim=l.limit_bytes===0?'∞':fmtB(l.limit_bytes);
  const pct=l.limit_bytes===0?0:Math.min(100,l.used_bytes/l.limit_bytes*100);
  const bc=pct>90?'var(--red)':pct>70?'var(--amber)':'var(--accent)';
  const allowed=l.active&&!l.expired;
  const cardCls=!l.active?'is-off':(l.expired?'is-exp':'');
  const checked=selectedLinks.has(l.uuid)?'checked':'';
  return `<div class="cfg-card ${cardCls}">
    <div class="cfg-row">
      <span class="cfg-select"><input type="checkbox" ${checked} onchange="toggleLinkSelect('${l.uuid}',this)" title="Select"></span>
      <span class="cfg-status-dot ${allowed?'pulse':''}"></span>
      <div class="cfg-identity">
        <div class="cfg-label">${esc(l.label)}</div>
        <div class="cfg-sub-meta">
          <span class="cfg-uuid-mini" onclick="navigator.clipboard.writeText('${l.uuid}').then(()=>toast('UUID copied','ok'))" title="${l.uuid}"><i class="ti ti-fingerprint"></i> ${l.uuid.slice(0,10)}…</span>
          <span>${new Date(l.created_at).toLocaleDateString('en-US')}</span>
        </div>
      </div>
      <div class="cfg-divider-v"></div>
      <div class="cfg-usage-col">
        <div class="ubar"><div class="ubar-f" style="width:${pct}%;background:${bc}"></div></div>
        <div class="utxt"><span>${fmtB(l.used_bytes)}</span><span>of ${lim}</span></div>
      </div>
      <div class="cfg-divider-v"></div>
      <div class="cfg-exp-col">${expChip(l.expires_at,l.expired)}</div>
      <div class="cfg-divider-v"></div>
      <div class="cfg-badges-col">
        ${protoBadge(l.protocol)}
        <span class="cfg-sub-tag" title="Connection port"><i class="ti ti-route"></i> :${l.port||443}</span>
        <span class="cfg-sub-tag" title="Fingerprint"><i class="ti ti-fingerprint"></i> ${esc(l.fingerprint||'chrome')}</span>
        <span class="cfg-sub-tag" title="Connected IPs / limit"><i class="ti ti-users"></i> ${l.connected_ips||0}${l.ip_limit?('/'+l.ip_limit):' (∞)'}</span>
        <span class="cfg-sub-tag" title="Speed limit"><i class="ti ti-gauge"></i> ${l.speed_limit_bytes?((l.speed_limit_bytes*8/1024/1024).toFixed(1)+' Mbps'):'Unlimited'}</span>
      </div>
      <div class="cfg-divider-v"></div>
      <div class="cfg-actions">
        <button class="tog${allowed?' on':''}" onclick="toggleActive('${l.uuid}',${!l.active})" title="Enable/Disable"></button>
        <button class="btn btn-sm btn-g btn-icon" onclick="navigator.clipboard.writeText('${esc(l.vless_link)}').then(()=>toast('Link copied','ok'))" title="Copy link"><i class="ti ti-copy"></i></button>
        <button class="btn btn-sm btn-g btn-icon" onclick="window.open('${esc(l.sub_url)}','_blank')" title="Open sub dashboard"><i class="ti ti-rss"></i></button>
        <button class="btn btn-sm btn-g btn-icon" onclick="showQR('${esc(l.vless_link)}')" title="QR"><i class="ti ti-qrcode"></i></button>
        <button class="btn btn-sm btn-g btn-icon" onclick="openLinkChart('${l.uuid}','${esc(l.label)}')" title="Usage chart, last 30 days"><i class="ti ti-chart-line"></i></button>
        <button class="btn btn-sm btn-amber btn-icon" onclick="openEditLink('${l.uuid}')" title="Edit"><i class="ti ti-edit"></i></button>
        <button class="btn btn-sm btn-g btn-icon" onclick="resetUsage('${l.uuid}')" title="Reset usage"><i class="ti ti-rotate"></i></button>
        <button class="btn btn-sm btn-d btn-icon" onclick="deleteLink('${l.uuid}')" title="Delete"><i class="ti ti-trash"></i></button>
      </div>
    </div>
  </div>`;
}).join('');
  updateBulkBar();
}
function toggleLinkSelect(uuid,el){
  if(el.checked)selectedLinks.add(uuid);else selectedLinks.delete(uuid);
  updateBulkBar();
}
function toggleSelectAllLinks(el){
  const list=filteredLinksList();
  if(el.checked)list.forEach(l=>selectedLinks.add(l.uuid));
  else list.forEach(l=>selectedLinks.delete(l.uuid));
  renderLinksGrid();
}
function clearLinksSelection(){selectedLinks.clear();renderLinksGrid();}
function updateBulkBar(){
  const bar=document.getElementById('links-bulkbar');
  const selall=document.getElementById('links-selall');
  const n=selectedLinks.size;
  document.getElementById('links-selcount').textContent=fmtNum(n);
  bar.style.display=n>0?'flex':'none';
  const list=filteredLinksList();
  selall.checked=list.length>0&&list.every(l=>selectedLinks.has(l.uuid));
}
async function bulkLinksAction(action){
  const uuids=Array.from(selectedLinks);
  if(!uuids.length)return;
  if(action==='delete'&&!confirm(`Delete ${fmtNum(uuids.length)} selected config(s)? This cannot be undone.`))return;
  try{
    await Promise.all(uuids.map(uuid=>{
      if(action==='activate')return authF('/api/links/'+uuid,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({active:true})});
      if(action==='deactivate')return authF('/api/links/'+uuid,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({active:false})});
      if(action==='reset')return authF('/api/links/'+uuid,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({reset_usage:true})});
      if(action==='delete')return authF('/api/links/'+uuid,{method:'DELETE'});
    }));
    const msg={activate:'Selected configs activated ✓',deactivate:'Selected configs deactivated ✓',reset:'Usage reset for selected configs ✓',delete:'Selected configs deleted ✓'}[action];
    toast(msg,'ok');
    if(action==='delete')selectedLinks.clear();
    loadLinks();
  }catch(e){toast('Bulk action failed','err')}
}
let linkChart=null;
async function openLinkChart(uuid,label){
  document.getElementById('lc-title').textContent='Usage chart, last 30 days — '+label;
  openModal('modal-link-chart');
  try{
    const r=await authF('/api/links/'+uuid+'/history'),d=await r.json();
    const labels=d.days.map(x=>x.date.slice(5));
    const vals=d.days.map(x=>+(x.bytes/1024**2).toFixed(2));
    const ctx=document.getElementById('lc-canvas');
    if(linkChart)linkChart.destroy();
    linkChart=new Chart(ctx,{type:'bar',data:{labels,datasets:[{label:'Usage (MB)',data:vals,backgroundColor:'rgba(135,145,161,.55)',borderRadius:5,maxBarThickness:22}]},
      options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{grid:{display:false}},y:{beginAtZero:true}}}});
  }catch(e){toast('Failed to load usage history','err')}
}
async function createLink(){
  const label=document.getElementById('nl-label').value.trim()||'New config';
  const val=document.getElementById('nl-val').value;
  const unit=document.getElementById('nl-unit').value;
  const exp=document.getElementById('nl-exp').value;
  const note=document.getElementById('nl-note').value.trim();
  const protocol=document.getElementById('nl-proto').value||'vless-ws';
  const fingerprint=document.getElementById('nl-fp').value||'chrome';
  const alpn=document.getElementById('nl-alpn').value.trim();
  const port=443;
  const ip_limit=Number(document.getElementById('nl-iplimit').value)||0;
  const speed_limit_value=Number(document.getElementById('nl-speed').value)||0;
  const speed_limit_unit=document.getElementById('nl-speed-unit').value;
  try{
    const r=await authF('/api/links',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({label,limit_value:val||0,limit_unit:unit,expires_days:exp||0,note,protocol,fingerprint,alpn,port,ip_limit,speed_limit_value,speed_limit_unit})});
    if(!r.ok)throw new Error('failed');
    ['nl-label','nl-val','nl-exp','nl-note','nl-alpn'].forEach(id=>document.getElementById(id).value='');
    document.getElementById('nl-iplimit').value='0';
    document.getElementById('nl-speed').value='0';
    document.getElementById('nl-alpn-preset').value='';
    document.getElementById('nl-alpn').style.display='none';
    toast('Config created ✓','ok');loadLinks();
  }catch(e){toast('Failed to create','err')}
}
function openEditLink(uuid){
  const l=allLinksList.find(x=>x.uuid===uuid);
  if(!l)return;
  document.getElementById('el-uuid').value=uuid;
  document.getElementById('el-label').value=l.label;
  document.getElementById('el-note').value=l.note||'';
  if(l.limit_bytes===0){document.getElementById('el-val').value='';document.getElementById('el-unit').value='GB';}
  else{document.getElementById('el-val').value=(l.limit_bytes/1024/1024).toFixed(0);document.getElementById('el-unit').value='MB';}
  document.getElementById('el-exp').value='';
  document.getElementById('el-fp').value=l.fingerprint||'chrome';
  document.getElementById('el-alpn').value=l.alpn||'';
  document.getElementById('el-port').value=l.port||443;
  document.getElementById('el-iplimit').value=l.ip_limit||0;
  if(!l.speed_limit_bytes){document.getElementById('el-speed').value='0';document.getElementById('el-speed-unit').value='MBIT';}
  else{document.getElementById('el-speed').value=(l.speed_limit_bytes*8/1024/1024).toFixed(2);document.getElementById('el-speed-unit').value='MBIT';}
  openModal('modal-edit-link');
}
async function saveEditLink(){
  const uuid=document.getElementById('el-uuid').value;
  const label=document.getElementById('el-label').value.trim();
  const note=document.getElementById('el-note').value.trim();
  const val=document.getElementById('el-val').value;
  const unit=document.getElementById('el-unit').value;
  const exp=document.getElementById('el-exp').value;
  const fingerprint=document.getElementById('el-fp').value||'chrome';
  const alpn=document.getElementById('el-alpn').value.trim();
  const port=Number(document.getElementById('el-port').value)||443;
  const ip_limit=Number(document.getElementById('el-iplimit').value)||0;
  const speed_limit_value=Number(document.getElementById('el-speed').value)||0;
  const speed_limit_unit=document.getElementById('el-speed-unit').value;
  const body={label,note,limit_value:val||0,limit_unit:unit,fingerprint,alpn,port,ip_limit,speed_limit_value,speed_limit_unit};
  if(exp&&Number(exp)>0)body.expires_days=Number(exp);
  try{
    const r=await authF('/api/links/'+uuid,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
    if(!r.ok)throw new Error();
    closeModal('modal-edit-link');
    toast('Config updated ✓','ok');loadLinks();
  }catch(e){toast('Failed to update','err')}
}
async function toggleActive(uuid,newState){
  try{const r=await authF('/api/links/'+uuid,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({active:newState})});if(!r.ok)throw new Error();toast(newState?'Activated ✓':'Deactivated','ok');loadLinks();}catch(e){toast('Error','err')}
}
async function resetUsage(uuid){
  try{const r=await authF('/api/links/'+uuid,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({reset_usage:true})});if(!r.ok)throw new Error();toast('Usage reset ✓','ok');loadLinks();}catch(e){toast('Error','err')}
}
async function deleteLink(uuid){
  if(!confirm('Delete this config?'))return;
  try{const r=await authF('/api/links/'+uuid,{method:'DELETE'});if(!r.ok)throw new Error();toast('Deleted ✓','ok');loadLinks();}catch(e){toast('Error','err')}
}
function showQR(link){window.open('https://api.qrserver.com/v1/create-qr-code/?size=300x300&data='+encodeURIComponent(link),'_blank')}
function parseBytesFmt(s){
  if(!s)return 0;
  const m=String(s).match(/([\d.]+)\s*([A-Za-z]+)/);
  if(!m)return 0;
  const n=parseFloat(m[1]),u=m[2].toUpperCase();
  const mult={B:1,KB:1024,MB:1024**2,GB:1024**3,TB:1024**4};
  return n*(mult[u]||1);
}
let connsExpanded=new Set();
function toggleConnCard(uuid){
  if(connsExpanded.has(uuid))connsExpanded.delete(uuid);else connsExpanded.add(uuid);
  renderConnsGrid(window.__lastConfigs||[]);
}
function renderConnsGrid(configs){
  const grid=document.getElementById('conns-grid');
  grid.innerHTML=configs.map(cfg=>{
    const open=connsExpanded.has(cfg.uuid);
    const ipsHtml=(cfg.connections||[]).map(c=>{
      const secs=c.connected_at?Math.max(0,Math.floor((Date.now()-new Date(c.connected_at).getTime())/1000)):0;
      const dur=secs<60?secs+' sec':secs<3600?Math.floor(secs/60)+' min':Math.floor(secs/3600)+' hr';
      return `<div style="display:flex;align-items:center;justify-content:space-between;gap:10px;padding:10px 12px;border-radius:10px;background:var(--accent-d);border:1px solid var(--card-b);margin-top:7px">
        <div style="display:flex;align-items:center;gap:8px;min-width:0">
          <i class="ti ti-device-desktop" style="color:var(--t3)"></i>
          <span style="font-family:IBM Plex Mono,ui-monospace,monospace;font-size:12px;color:var(--t1)">${esc(c.ip)}</span>
          <button class="conn-ip-copy" onclick="navigator.clipboard.writeText('${esc(c.ip)}').then(()=>toast('IP copied','ok'))" title="Copy IP"><i class="ti ti-copy"></i></button>
        </div>
        <div style="display:flex;align-items:center;gap:12px;font-size:10.5px;color:var(--t3);flex-shrink:0">
          <span><i class="ti ti-repeat" style="font-size:10px"></i> ${fmtNum(c.sessions)} sessions</span>
          <span><i class="ti ti-transfer" style="font-size:10px"></i> ${esc(c.bytes_fmt)}</span>
          <span><i class="ti ti-clock" style="font-size:10px"></i> ${dur}</span>
        </div>
      </div>`;
    }).join('') || '<div style="padding:10px;color:var(--t3);font-size:11px">No connections</div>';
    return `<div class="conn-card-v2" style="cursor:pointer" onclick="toggleConnCard('${cfg.uuid}')">
      <div class="conn-card-v2-glow"></div>
      <div class="conn-card-v2-top">
        <div class="conn-avatar"><i class="ti ti-key"></i></div>
        <div class="conn-card-v2-id">
          <div class="conn-ip-v2">${esc(cfg.label)}</div>
          <div class="conn-label-v2">${fmtNum(cfg.ip_count)} IPs · ${fmtNum(cfg.sessions)} sessions</div>
        </div>
        <span class="conn-status-pill"><span class="dot dg pulse"></span> Live</span>
      </div>
      <div class="conn-card-v2-divider"></div>
      <div class="conn-card-v2-body">
        <div class="conn-proto-row">${protoBadge(cfg.protocol)}</div>
        <div class="conn-stat-row">
          <div class="conn-stat-box">
            <div class="conn-stat-icon"><i class="ti ti-transfer"></i></div>
            <div>
              <div class="conn-stat-text-label">Traffic</div>
              <div class="conn-stat-text-val">${esc(cfg.bytes_fmt)}</div>
            </div>
          </div>
          <div class="conn-stat-box">
            <div class="conn-stat-icon time"><i class="ti ti-users"></i></div>
            <div>
              <div class="conn-stat-text-label">Connected IPs</div>
              <div class="conn-stat-text-val">${fmtNum(cfg.ip_count)}</div>
            </div>
          </div>
        </div>
        <div style="text-align:center;font-size:10.5px;color:var(--accent2);margin-top:8px"><i class="ti ti-chevron-${open?'up':'down'}"></i> ${open?'Hide':'Show connections'}</div>
        ${open?`<div onclick="event.stopPropagation()">${ipsHtml}</div>`:''}
      </div>
    </div>`;
  }).join('');
}
async function loadConns(){
  try{
    const r=await authF('/api/connections'),d=await r.json();
    const grid=document.getElementById('conns-grid'),ce=document.getElementById('conns-empty');
    document.getElementById('conns-live').innerHTML='<span class="dot dg pulse"></span> '+d.raw_count+' connections';
    document.getElementById('ch-count').textContent=fmtNum(d.raw_count);
    const configs=d.configs||[];
    window.__lastConfigs=configs;
    if(!configs.length){
      grid.innerHTML='';ce.style.display='block';
      document.getElementById('ch-traffic').textContent='—';
      document.getElementById('ch-avgdur').textContent='—';
      document.getElementById('ch-uniq').textContent='—';
      return;
    }
    ce.style.display='none';
    const totalBytes=configs.reduce((s,c)=>s+(c.bytes||0),0);
    document.getElementById('ch-traffic').textContent=fmtB(totalBytes);
    const uniqIps=configs.reduce((s,c)=>s+c.ip_count,0);
    document.getElementById('ch-uniq').textContent=fmtNum(uniqIps);
    const allDurs=[];
    configs.forEach(c=>(c.connections||[]).forEach(ip=>allDurs.push(ip.connected_at?Math.max(0,Math.floor((Date.now()-new Date(ip.connected_at).getTime())/1000)):0)));
    const avgSec=allDurs.length?Math.floor(allDurs.reduce((a,b)=>a+b,0)/allDurs.length):0;
    document.getElementById('ch-avgdur').textContent=avgSec<60?avgSec+' s':avgSec<3600?Math.floor(avgSec/60)+' m':Math.floor(avgSec/3600)+' h';
    renderConnsGrid(configs);
  }catch(e){console.error(e)}
}

// ── داشبورد کانفیگ‌ها: از داده‌ی همون /api/links و /api/connections استفاده می‌کنه ──
let cfgDashSelected=null;
async function loadCfgDash(){
  try{
    if(!allLinksList.length)await loadLinks();
    await loadConns();
    renderCfgDashList();
    if(cfgDashSelected&&allLinksList.some(l=>l.uuid===cfgDashSelected))renderCfgDashDetail(cfgDashSelected);
  }catch(e){console.error(e)}
}
function renderCfgDashList(){
  const wrap=document.getElementById('cfgdash-list'),empty=document.getElementById('cfgdash-empty');
  document.getElementById('cfgdash-count').textContent=fmtNum(allLinksList.length);
  if(!allLinksList.length){wrap.innerHTML='';empty.style.display='block';return}
  empty.style.display='none';
  wrap.innerHTML=allLinksList.map(l=>{
    const allowed=l.active&&!l.expired;
    const pct=l.limit_bytes===0?0:Math.min(100,l.used_bytes/l.limit_bytes*100);
    const bc=pct>90?'var(--red)':pct>70?'var(--amber)':'var(--accent)';
    return `<div class="cfgdash-item${cfgDashSelected===l.uuid?' on':''}" onclick="selectCfgDash('${l.uuid}')">
      <div class="cfgdash-item-top"><span class="cfg-status-dot ${allowed?'pulse':''}"></span><span class="cfgdash-item-label">${esc(l.label)}</span>${protoBadge(l.protocol)}</div>
      <div class="ubar"><div class="ubar-f" style="width:${pct}%;background:${bc}"></div></div>
      <div class="utxt"><span>${fmtB(l.used_bytes)}</span><span>${l.connected_ips||0} IPs online</span></div>
    </div>`;
  }).join('');
}
function selectCfgDash(uuid){cfgDashSelected=uuid;renderCfgDashList();renderCfgDashDetail(uuid)}
function renderCfgDashDetail(uuid){
  const box=document.getElementById('cfgdash-detail');
  const l=allLinksList.find(x=>x.uuid===uuid);
  if(!l){box.innerHTML='<div class="card"><div class="empty"><i class="ti ti-mood-empty"></i><p>This config no longer exists</p></div></div>';return}
  const grp=(window.__lastConfigs||[]).find(c=>c.uuid===uuid);
  const ips=grp?grp.connections||[]:[];
  const pct=l.limit_bytes===0?0:Math.min(100,l.used_bytes/l.limit_bytes*100);
  const bc=pct>90?'var(--red)':pct>70?'var(--amber)':'var(--accent)';
  const speedTxt=l.speed_limit_bytes?((l.speed_limit_bytes*8/1024/1024).toFixed(1)+' Mbps'):'Unlimited';
  box.innerHTML=`
    <div class="card" style="margin-bottom:14px">
      <div class="card-title"><i class="ti ti-key"></i> ${esc(l.label)} ${l.active&&!l.expired?'<span class="badge bg-green" style="margin-left:6px">Active</span>':'<span class="badge bg-red" style="margin-left:6px">'+(l.expired?'Expired':'Inactive')+'</span>'}
        <span class="ml-auto" style="display:flex;gap:6px">
          <button class="btn btn-sm btn-g btn-icon" onclick="navigator.clipboard.writeText('${esc(l.vless_link)}').then(()=>toast('Link copied','ok'))" title="Copy link"><i class="ti ti-copy"></i></button>
          <button class="btn btn-sm btn-g btn-icon" onclick="showQR('${esc(l.vless_link)}')" title="QR"><i class="ti ti-qrcode"></i></button>
          <button class="btn btn-sm btn-g btn-icon" onclick="openLinkChart('${l.uuid}','${esc(l.label)}')" title="Usage chart"><i class="ti ti-chart-line"></i></button>
        </span>
      </div>
      <div class="cfgdash-stats">
        <div class="cfgdash-stat"><div class="cfgdash-stat-l">Usage / limit</div><div class="cfgdash-stat-v">${fmtB(l.used_bytes)}</div><div class="utxt" style="margin-top:6px"><span></span><span>of ${l.limit_bytes===0?'∞':fmtB(l.limit_bytes)}</span></div><div class="ubar" style="margin-top:6px"><div class="ubar-f" style="width:${pct}%;background:${bc}"></div></div></div>
        <div class="cfgdash-stat"><div class="cfgdash-stat-l">Speed limit</div><div class="cfgdash-stat-v" style="font-size:14px">${speedTxt}</div></div>
        <div class="cfgdash-stat"><div class="cfgdash-stat-l">Live IPs / limit</div><div class="cfgdash-stat-v">${fmtNum(l.connected_ips||0)}${l.ip_limit?(' / '+fmtNum(l.ip_limit)):' (∞)'}</div></div>
        <div class="cfgdash-stat"><div class="cfgdash-stat-l">Expiry</div><div class="cfgdash-stat-v" style="font-size:14px">${expChip(l.expires_at,l.expired)}</div></div>
      </div>
      <div class="sr"><span class="sr-k"><i class="ti ti-route"></i> Protocol</span><span class="sr-v">${protoBadge(l.protocol)}</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-plug"></i> Port</span><span class="sr-v">${fmtNum(l.port||443)}</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-fingerprint"></i> Fingerprint</span><span class="sr-v">${esc(l.fingerprint||'chrome')}</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-calendar"></i> Created</span><span class="sr-v">${new Date(l.created_at).toLocaleDateString('en-US')}</span></div>
    </div>
    <div class="card">
      <div class="card-title"><i class="ti ti-map-pin"></i> Currently connected IPs <span class="ml-auto badge bg-blue">${fmtNum(ips.length)}</span></div>
      ${ips.length?ips.map(c=>{
        const secs=c.connected_at?Math.max(0,Math.floor((Date.now()-new Date(c.connected_at).getTime())/1000)):0;
        const dur=secs<60?secs+' sec':secs<3600?Math.floor(secs/60)+' min':Math.floor(secs/3600)+' hr';
        return `<div class="cfgdash-ip-row">
          <span class="ip"><span class="dot dg pulse" style="width:7px;height:7px;border-radius:50%;background:var(--green);display:inline-block"></span> ${esc(c.ip)}</span>
          <div class="cfgdash-ip-meta">
            <span><i class="ti ti-repeat"></i> ${fmtNum(c.sessions)} sessions</span>
            <span><i class="ti ti-transfer"></i> ${esc(c.bytes_fmt)}</span>
            <span><i class="ti ti-clock"></i> ${dur}</span>
          </div>
        </div>`;
      }).join(''):'<div class="empty"><i class="ti ti-plug-off"></i><p>No IPs are currently connected to this config</p></div>'}
    </div>
  `;
}

async function loadErrs(){try{const r=await authF('/stats'),d=await r.json();renderErrs(d.recent_errors||[]);}catch(e){}}
function cpText(id){navigator.clipboard.writeText(document.getElementById(id).textContent).then(()=>toast('Copied ✓','ok'))}
function qrFor(id){showQR(document.getElementById(id).textContent)}
function refreshAll(){fetchStats();loadLinks();if(document.getElementById('pg-connections').classList.contains('on'))loadConns();if(document.getElementById('pg-logs').classList.contains('on'))loadActivity();toast('Refreshed','ok')}
async function changePw(){
  const cur=document.getElementById('cp-cur').value,nw=document.getElementById('cp-new').value,cf=document.getElementById('cp-cf').value;
  if(!cur||!nw||!cf){toast('Fill in all fields','err');return}
  if(nw.length<4){toast('At least 4 characters','err');return}
  if(nw!==cf){toast('Passwords do not match','err');return}
  try{
    const r=await authF('/api/change-password',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({current_password:cur,new_password:nw})});
    const d=await r.json().catch(()=>({}));
    if(!r.ok)throw new Error(d.detail||'Error');
    toast('Password changed ✓','ok');
    ['cp-cur','cp-new','cp-cf'].forEach(id=>document.getElementById(id).value='');
  }catch(e){toast('✗ '+e.message,'err')}
}
function togglePwField(id,btn){
  const inp=document.getElementById(id);
  const icon=btn.querySelector('i');
  const toText=inp.type==='password';
  inp.type=toText?'text':'password';
  icon.className='ti '+(toText?'ti-eye-off':'ti-eye');
}
function checkPwStrength(val){
  const segs=document.querySelectorAll('#pw-strength-bar .pw-strength-seg');
  const label=document.getElementById('pw-strength-label');
  const reqLen=document.getElementById('req-len'),reqNum=document.getElementById('req-num'),reqCase=document.getElementById('req-case');
  const hasLen=val.length>=4,hasNum=/\d/.test(val),hasCase=/[a-z]/.test(val)&&/[A-Z]/.test(val),hasLong=val.length>=8;
  reqLen.classList.toggle('met',hasLen);
  reqNum.classList.toggle('met',hasNum);
  reqCase.classList.toggle('met',hasCase);
  let score=0;if(hasLen)score++;if(hasNum)score++;if(hasCase)score++;if(hasLong)score++;
  const colors=['#d9605a','#c99a3c','#6f9cf0','#3fa77a'],labels=['Very weak','Weak','Medium','Strong'];
  segs.forEach((s,i)=>{s.style.background=i<score?colors[Math.max(0,score-1)]:'rgba(100,116,139,.2)'});
  if(val.length===0){label.innerHTML='<i class="ti ti-shield"></i> Password strength';return}
  label.innerHTML=`<i class="ti ti-shield-check" style="color:${colors[Math.max(0,score-1)]}"></i> ${labels[Math.max(0,score-1)]}`;
}
function makeGradient(ctx,color1,color2){
  const g=ctx.createLinearGradient(0,0,0,260);
  g.addColorStop(0,color1);g.addColorStop(1,color2);
  return g;
}
function initCharts(){
  const c1=document.getElementById('ch1').getContext('2d');
  const grad1=makeGradient(c1,'rgba(111,156,240,.38)','rgba(111,156,240,0)');
  const opts={
    responsive:true,maintainAspectRatio:false,
    interaction:{mode:'index',intersect:false},
    plugins:{
      legend:{display:false},
      tooltip:{
        backgroundColor:'rgba(26,29,34,.97)',borderColor:'rgba(111,156,240,.3)',borderWidth:1,
        titleColor:'#e5e8ec',bodyColor:'#a5adb9',padding:11,cornerRadius:4,displayColors:false,
        titleFont:{family:'IBM Plex Sans',size:11,weight:'700'},bodyFont:{family:'IBM Plex Sans',size:11},
        callbacks:{label:v=>`${v.parsed.y.toFixed(2)} MB`}
      }
    },
    scales:{
      x:{grid:{display:false},border:{display:false},ticks:{color:'#707988',font:{size:9,family:'IBM Plex Sans'}}},
      y:{grid:{color:'rgba(111,156,240,.06)'},border:{display:false},ticks:{color:'#707988',font:{size:9,family:'IBM Plex Sans'},callback:v=>v+' MB'}}
    },
    elements:{line:{capBezierPoints:true}}
  };
  const ds1={label:'MB',data:[],borderColor:'#6f9cf0',backgroundColor:grad1,fill:true,tension:.42,pointRadius:0,pointHoverRadius:6,pointHoverBackgroundColor:'#6f9cf0',pointHoverBorderColor:'#fff',pointHoverBorderWidth:2,borderWidth:2.5};
  ch1=new Chart(document.getElementById('ch1'),{type:'line',data:{labels:[],datasets:[ds1]},options:opts});

  function makeGradientV2(ctx,c1,c2,c3){
    const g=ctx.createLinearGradient(0,0,0,320);
    g.addColorStop(0,c1);g.addColorStop(.6,c2);g.addColorStop(1,c3);
    return g;
  }
  const c3ctx=document.getElementById('ch3').getContext('2d');
  const gradFill3=makeGradientV2(c3ctx,'rgba(111,156,240,.45)','rgba(111,156,240,.08)','rgba(111,156,240,0)');
  ch3=new Chart(document.getElementById('ch3'),{
    type:'line',
    data:{labels:[],datasets:[
      {label:'Usage',data:[],borderColor:'#6f9cf0',backgroundColor:gradFill3,fill:true,tension:.45,pointRadius:0,pointHoverRadius:7,pointHoverBackgroundColor:'#fff',pointHoverBorderColor:'#6f9cf0',pointHoverBorderWidth:3,borderWidth:3,order:2},
      {label:'Average',data:[],borderColor:'#c99a3c',borderDash:[6,5],borderWidth:1.6,pointRadius:0,fill:false,tension:0,order:1}
    ]},
    options:{
      responsive:true,maintainAspectRatio:false,
      interaction:{mode:'index',intersect:false},
      plugins:{
        legend:{display:false},
        tooltip:{
          backgroundColor:'rgba(26,29,34,.97)',borderColor:'rgba(111,156,240,.35)',borderWidth:1,
          titleColor:'#e5e8ec',bodyColor:'#a5adb9',padding:13,cornerRadius:4,displayColors:true,boxPadding:4,
          titleFont:{family:'IBM Plex Sans',size:11.5,weight:'700'},bodyFont:{family:'IBM Plex Sans',size:11},
          callbacks:{label:v=>` ${v.dataset.label}: ${v.parsed.y.toFixed(2)} MB`}
        }
      },
      scales:{
        x:{grid:{display:false},border:{display:false},ticks:{color:'#707988',font:{size:9.5,family:'IBM Plex Sans'},maxRotation:0}},
        y:{grid:{color:'rgba(111,156,240,.05)'},border:{display:false},ticks:{color:'#707988',font:{size:9.5,family:'IBM Plex Sans'},callback:v=>v+' MB'}}
      }
    }
  });

  ch2=new Chart(document.getElementById('ch2'),{
    type:'doughnut',
    data:{labels:['VLESS/WS','XHTTP Ultra','HTTP Proxy'],datasets:[{
      data:[55,35,10],
      backgroundColor:['#6f9cf0','#3fa77a','#8791a1'],
      borderColor:getComputedStyle(document.documentElement).getPropertyValue('--card')||'#1a1d22',
      borderWidth:4,hoverOffset:10,borderRadius:6,spacing:3
    }]},
    options:{
      responsive:true,maintainAspectRatio:false,cutout:'72%',
      plugins:{
        legend:{position:'bottom',labels:{color:'var(--t2)',font:{size:10,family:'IBM Plex Sans'},padding:12,usePointStyle:true,pointStyle:'circle'}},
        tooltip:{backgroundColor:'rgba(26,29,34,.97)',borderColor:'rgba(111,156,240,.3)',borderWidth:1,padding:10,cornerRadius:4,bodyFont:{family:'IBM Plex Sans'},titleFont:{family:'IBM Plex Sans'}}
      }
    }
  });
}
let ws;
function wsLog(c,m){const l=document.getElementById('ws-log'),p=document.createElement('p');const colors={ok:'#6fcb9f',err:'#ef8c87',info:'#a5adb9',sent:'#e2bd70'};p.style.color=colors[c]||'#fff';p.textContent='['+new Date().toLocaleTimeString('en-US')+'] '+m;l.appendChild(p);l.scrollTop=l.scrollHeight}
function wsConn(){const u=document.getElementById('ws-uuid').value.trim();if(!u){toast('Enter a UUID','err');return}const url=(location.protocol==='https:'?'wss':'ws')+'://'+location.host+'/ws/'+u;wsLog('info','Connecting: '+url);ws=new WebSocket(url);ws.onopen=()=>wsLog('ok','✓ Connected - valid UUID');ws.onerror=()=>wsLog('err','✗ Error - invalid or inactive UUID');ws.onmessage=m=>wsLog('info','Received '+(m.data.size||m.data.length)+' byte');ws.onclose=e=>wsLog('err','Disconnected ('+e.code+')'+(e.code===1008?' - access denied':''))}
function wsSend(){const m=document.getElementById('ws-msg').value;if(!m||!ws||ws.readyState!==1)return;ws.send(m);wsLog('sent','Sent: '+m);document.getElementById('ws-msg').value=''}
function wsDisc(){if(ws)ws.close()}
document.addEventListener('DOMContentLoaded',async()=>{
  await checkAuth();
  initCharts();
  document.getElementById('set-host').textContent=location.host;
  fetchStats();loadLinks();
  setInterval(fetchStats,4000);
  setInterval(()=>{
    if(document.getElementById('pg-links').classList.contains('on'))loadLinks();
    if(document.getElementById('pg-connections').classList.contains('on'))loadConns();
    if(document.getElementById('pg-logs').classList.contains('on'))loadActivity();
    if(document.getElementById('pg-cfgdash').classList.contains('on'))loadCfgDash();
  },5000);
});
</script>
</body></html>"""


# جایگزینی نهایی لوگو در صفحات استاتیک (LOGIN_HTML / DASHBOARD_HTML)

def get_public_page_html(uuid_key: str) -> str:
    """Public sub page v3 — refined design: config link hidden behind a show button, dedicated password page"""
    return f"""<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<title>Panel Sub</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>
*{{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}}
:root{{
  --bg:#121417;--bg2:#171a1e;--bg3:#1e2227;--card:#1a1d22;--card-b:#2a2f36;--card-bh:#3b424c;--accent:#6f9cf0;--accent2:#9bb8f4;--accent-s:#3f73d9;--accent-d:rgba(111,156,240,0.10);--green:#3fa77a;--green-bg:rgba(63,167,122,0.12);--green-t:#6fcb9f;--red:#d9605a;--red-bg:rgba(217,96,90,0.12);--red-t:#ef8c87;--amber:#c99a3c;--amber-bg:rgba(201,154,60,0.12);--amber-t:#e2bd70;--purple:#8791a1;--purple-bg:rgba(135,145,161,0.14);--purple-t:#a3acb9;--t1:#e5e8ec;--t2:#a5adb9;--t3:#707988;--input:#14171b;--radius:6px;--shadow:none;--serif:'IBM Plex Sans',system-ui,sans-serif;
}}
[data-theme="light"]{{
  --bg:#f2f3f5;--bg2:#e9ebee;--bg3:#e0e3e7;--card:#ffffff;--card-b:#d5d9df;--card-bh:#b9bfc8;--accent:#2f62c4;--accent2:#244e9f;--accent-s:#2f62c4;--accent-d:rgba(47,98,196,0.08);--green:#1f8a5e;--green-bg:rgba(31,138,94,0.10);--green-t:#176e4b;--red:#c0392f;--red-bg:rgba(192,57,47,0.09);--red-t:#9e2c24;--amber:#b07d1a;--amber-bg:rgba(176,125,26,0.10);--amber-t:#80590f;--purple:#5f6b7d;--purple-bg:rgba(95,107,125,0.10);--purple-t:#4a5565;--t1:#1b1f24;--t2:#454d59;--t3:#7a828e;--input:#ffffff;--shadow:none;
}}
html,body{{min-height:100%;background:var(--bg);font-family:var(--serif);color:var(--t1);font-size:14px;transition:background .35s,color .35s}}
.bg-fx{{position:fixed;inset:0;background:radial-gradient(ellipse 70% 45% at 50% -8%,rgba(111,156,240,0.13),transparent 62%),var(--bg);z-index:0;pointer-events:none;transition:background .35s}}
.grid-fx{{position:fixed;inset:0;background-image:linear-gradient(rgba(111,156,240,0.025) 1px,transparent 1px),linear-gradient(90deg,rgba(111,156,240,0.025) 1px,transparent 1px);background-size:46px 46px;z-index:0;pointer-events:none}}
.wrap{{position:relative;z-index:10;max-width:800px;margin:0 auto;padding:24px 16px 64px}}
.top{{display:flex;align-items:center;justify-content:space-between;margin-bottom:26px;gap:10px}}
.brand{{display:flex;align-items:center;gap:11px;min-width:0}}
.brand-img{{width:40px;height:40px;border-radius:50%;overflow:hidden;border:1px solid var(--card-b);box-shadow:0 0 14px rgba(135,145,161,.3),0 0 8px rgba(111,156,240,.25);flex-shrink:0}}
.brand-img img{{width:100%;height:100%;object-fit:cover}}
.brand-name{{font-size:14.5px;font-weight:800;color:var(--t1);letter-spacing:-.01em}}
.brand-sub{{font-size:9.5px;color:var(--t3);font-weight:500}}
.top-actions{{display:flex;align-items:center;gap:6px;flex-shrink:0}}
.icon-btn{{width:36px;height:36px;border-radius:11px;background:var(--card);border:1px solid var(--card-b);color:var(--t2);display:flex;align-items:center;justify-content:center;font-size:16px;cursor:pointer;transition:.18s}}
.icon-btn:hover{{background:var(--accent-d);color:var(--accent2);border-color:var(--card-bh)}}

.sub-info{{background:var(--card);border:1px solid var(--card-b);border-radius:22px;padding:24px 24px 22px;margin-bottom:16px;box-shadow:var(--shadow);position:relative;overflow:hidden}}
.sub-info::before{{content:'';position:absolute;top:0;left:0;width:160px;height:160px;background:radial-gradient(circle at top left,rgba(111,156,240,.1),transparent 70%);pointer-events:none}}
.sub-eyebrow{{font-size:10px;font-weight:700;color:var(--accent2);text-transform:uppercase;letter-spacing:.12em;margin-bottom:8px;display:flex;align-items:center;gap:6px}}
.sub-eyebrow i{{font-size:13px}}
.sub-name{{font-size:23px;font-weight:800;color:var(--t1);margin-bottom:6px;letter-spacing:-.02em}}
.sub-desc{{font-size:12.5px;color:var(--t2);line-height:1.8;margin-bottom:14px}}
.sub-meta-row{{font-size:10.5px;color:var(--t3);margin-bottom:14px;display:flex;align-items:center;gap:6px}}
.sub-sub-box{{background:var(--accent-d);border:1px solid var(--card-b);border-radius:13px;padding:12px 14px;display:flex;align-items:center;gap:9px;flex-wrap:wrap}}
.sub-sub-url{{font-family:IBM Plex Mono,ui-monospace,monospace;font-size:10px;color:var(--accent2);word-break:break-all;flex:1;min-width:140px}}

.stats-bar{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:18px}}
.stat-card{{background:var(--card);border:1px solid var(--card-b);border-radius:16px;padding:16px 17px;transition:.2s}}
.stat-card:hover{{border-color:var(--card-bh);transform:translateY(-1px)}}
.stat-label{{font-size:9px;color:var(--t3);font-weight:700;text-transform:uppercase;letter-spacing:.07em;margin-bottom:7px}}
.stat-val{{font-size:22px;font-weight:800;color:var(--t1);line-height:1;letter-spacing:-.01em}}
.stat-sub{{font-size:9.5px;color:var(--t3);margin-top:6px}}

.copy-all-bar{{display:flex;align-items:center;gap:12px;background:linear-gradient(120deg,var(--accent) 0%,#2952C8 100%);border-radius:18px;padding:16px 19px;margin-bottom:18px;box-shadow:0 10px 30px rgba(111,156,240,.28);flex-wrap:wrap}}
.copy-all-text{{flex:1;min-width:160px}}
.copy-all-title{{font-size:13.5px;font-weight:800;color:#fff;display:flex;align-items:center;gap:6px}}
.copy-all-sub{{font-size:10px;color:rgba(255,255,255,.78);margin-top:3px}}
.copy-all-btn{{background:#fff;color:#1D4ED8;border:none;border-radius:12px;padding:10px 19px;font-family:inherit;font-size:12.5px;font-weight:800;cursor:pointer;display:flex;align-items:center;gap:6px;transition:.18s;white-space:nowrap}}
.copy-all-btn:hover{{transform:translateY(-1px);box-shadow:0 6px 16px rgba(0,0,0,.22)}}
.copy-all-btn:active{{transform:translateY(0) scale(.98)}}

.cfg-title{{font-size:12px;font-weight:800;color:var(--t2);margin-bottom:13px;display:flex;align-items:center;gap:6px;text-transform:uppercase;letter-spacing:.07em}}
.cfg-title i{{color:var(--accent);font-size:15px}}
.cfg-grid{{display:grid;gap:13px}}

/* ── کارت کانفیگ به‌شکل بلیط دسترسی (signature element) ── */
.cfg-card{{background:var(--card);border:1px solid var(--card-b);border-radius:18px;transition:all .2s;position:relative;overflow:hidden}}
.cfg-card:hover{{border-color:var(--card-bh);box-shadow:var(--shadow)}}
.cfg-top{{padding:17px 19px 15px;position:relative}}
.cfg-top::after{{content:'';position:absolute;top:0;left:0;width:3px;height:100%;background:var(--green)}}
.cfg-card.inactive .cfg-top::after{{background:var(--red)}}
.cfg-head{{display:flex;align-items:flex-start;justify-content:space-between;gap:8px;margin-bottom:12px;flex-wrap:wrap}}
.cfg-label{{font-size:14.5px;font-weight:700;color:var(--t1)}}
.cfg-badges{{display:flex;gap:5px;flex-wrap:wrap;margin-top:6px}}
.proto-chip{{font-size:9px;padding:3px 8px;border-radius:7px;font-weight:800;letter-spacing:.02em}}
.pc-ws{{background:var(--accent-d);color:var(--accent2)}}
.pc-xhttp{{background:var(--purple-bg);color:var(--purple-t)}}
.pc-ultra{{background:var(--green-bg);color:var(--green-t)}}
.cfg-status{{display:flex;align-items:center;gap:5px;font-size:10px;font-weight:700;padding:4px 10px;border-radius:20px;white-space:nowrap}}
.cfg-status.ok{{background:var(--green-bg);color:var(--green-t)}}
.cfg-status.no{{background:var(--red-bg);color:var(--red-t)}}
.cfg-usage{{margin-bottom:4px}}
.ubar{{height:6px;border-radius:4px;background:rgba(111,156,240,0.1);overflow:hidden;margin-bottom:5px}}
.ubar-f{{height:100%;border-radius:4px;transition:width .5s ease}}
.utxt{{font-size:10px;color:var(--t3);display:flex;justify-content:space-between}}

/* خط جداکننده‌ی بلیطی با دندانه‌های گرد، شبیه پاره‌خط بُرد بلیط */
.cfg-tear{{position:relative;height:0;border-top:1.5px dashed var(--card-b);margin:0 19px}}
.cfg-tear::before,.cfg-tear::after{{content:'';position:absolute;top:50%;width:18px;height:18px;border-radius:50%;background:var(--bg);transform:translateY(-50%);border:1px solid var(--card-b)}}
.cfg-tear::before{{left:-28px}}
.cfg-tear::after{{right:-28px}}

.cfg-bottom{{padding:15px 19px 18px}}
.cfg-link-toggle{{width:100%;display:flex;align-items:center;justify-content:space-between;gap:10px;background:transparent;border:1px dashed var(--card-b);border-radius:11px;padding:10px 13px;cursor:pointer;font-family:inherit;color:var(--t2);font-size:11.5px;font-weight:600;transition:.15s}}
.cfg-link-toggle:hover{{background:var(--accent-d);border-color:var(--card-bh);color:var(--accent2)}}
.cfg-link-toggle .ltl{{display:flex;align-items:center;gap:7px}}
.cfg-link-toggle i.ti-chevron-down{{transition:transform .2s}}
.cfg-link-toggle.open i.ti-chevron-down{{transform:rotate(180deg)}}
.cfg-vless-wrap{{display:grid;grid-template-rows:0fr;transition:grid-template-rows .25s ease}}
.cfg-vless-wrap.open{{grid-template-rows:1fr}}
.cfg-vless-inner{{overflow:hidden}}
.cfg-vless{{background:rgba(0,0,0,.22);border:1px solid var(--card-b);border-radius:10px;padding:11px 13px;font-size:9.8px;font-family:IBM Plex Mono,ui-monospace,monospace;color:var(--accent2);word-break:break-all;line-height:1.7;margin-top:9px;max-height:90px;overflow-y:auto}}
[data-theme="light"] .cfg-vless{{background:rgba(47,98,196,.05)}}
.cfg-actions{{display:flex;gap:7px;flex-wrap:wrap;margin-top:11px}}
.btn{{font-family:inherit;font-size:11.5px;font-weight:700;border-radius:10px;padding:8px 15px;cursor:pointer;display:inline-flex;align-items:center;gap:5px;border:none;transition:all .15s;white-space:nowrap}}
.btn i{{font-size:13px}}
.btn-p{{background:linear-gradient(135deg,#2F8FFF,#8791a1);color:#fff;box-shadow:0 3px 14px rgba(135,145,161,.35)}}
.btn-p:hover{{background:var(--accent2)}}
.btn-g{{background:var(--accent-d);color:var(--accent2);border:1px solid rgba(111,156,240,.16)}}
.btn-g:hover{{background:rgba(111,156,240,.2)}}
.btn-pur{{background:var(--purple-bg);color:var(--purple-t);border:1px solid rgba(135,145,161,.2)}}
.btn-pur:hover{{background:rgba(135,145,161,.22)}}
.conn-chip{{display:inline-flex;align-items:center;gap:4px;font-size:9.5px;padding:3px 8px;border-radius:20px;background:var(--green-bg);color:var(--green-t);font-weight:700}}
.dot{{width:5px;height:5px;border-radius:50%;background:var(--green);display:inline-block;animation:pulse 2s infinite}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.25}}}}

/* ── صفحه‌ی قفل / رمز ── */
.lock-stage{{display:flex;align-items:center;justify-content:center;min-height:78vh;padding:20px 0}}
.lock-card{{background:var(--card);border:1px solid var(--card-b);border-radius:26px;padding:0;text-align:center;max-width:380px;width:100%;box-shadow:var(--shadow);overflow:hidden;position:relative}}
.lock-banner{{background:linear-gradient(150deg,rgba(111,156,240,.16),rgba(111,156,240,.02) 70%);padding:38px 30px 26px;position:relative}}
.lock-shield{{width:64px;height:64px;border-radius:18px;background:var(--accent-d);border:1px solid var(--card-bh);display:flex;align-items:center;justify-content:center;margin:0 auto 18px;position:relative}}
.lock-shield::after{{content:'';position:absolute;inset:-7px;border-radius:22px;border:1px solid var(--card-b);animation:breathe 2.6s ease-in-out infinite}}
@keyframes breathe{{0%,100%{{transform:scale(1);opacity:.5}}50%{{transform:scale(1.08);opacity:0}}}}
.lock-shield i{{font-size:28px;color:var(--accent2)}}
.lock-title{{font-size:18px;font-weight:800;margin-bottom:6px;color:var(--t1);letter-spacing:-.01em}}
.lock-sub{{font-size:12px;color:var(--t3);line-height:1.7}}
.lock-form{{padding:24px 30px 30px}}
.lock-field{{position:relative;margin-bottom:13px}}
.lock-inp{{width:100%;padding:13px 44px 13px 44px;border-radius:13px;border:1px solid var(--card-b);background:rgba(0,0,0,.2);color:var(--t1);font-family:inherit;font-size:14px;outline:none;text-align:center;letter-spacing:.14em;transition:.18s}}
[data-theme="light"] .lock-inp{{background:rgba(47,98,196,.04)}}
.lock-inp:focus{{border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-d)}}
.lock-eye{{position:absolute;right:13px;top:50%;transform:translateY(-50%);background:none;border:none;color:var(--t3);cursor:pointer;font-size:16px;padding:4px;display:flex}}
.lock-eye:hover{{color:var(--accent2)}}
.lock-lockicon{{position:absolute;left:14px;top:50%;transform:translateY(-50%);color:var(--t3);font-size:15px;pointer-events:none}}
.lock-err{{color:var(--red-t);font-size:11.5px;margin-bottom:10px;min-height:16px;display:flex;align-items:center;justify-content:center;gap:5px}}
.lock-btn{{width:100%;justify-content:center;padding:13px;font-size:13px;border-radius:13px}}
.lock-footer{{padding:14px 30px;border-top:1px solid var(--card-b);font-size:10px;color:var(--t3);display:flex;align-items:center;justify-content:center;gap:6px}}

.empty-state{{text-align:center;padding:80px 20px;color:var(--t3)}}
.empty-state i{{font-size:38px;display:block;margin-bottom:14px}}

.toast{{position:fixed;bottom:22px;left:50%;transform:translateX(-50%) translateY(40px);background:var(--card);border:1px solid var(--card-b);color:var(--t1);border-radius:12px;padding:10px 20px;font-size:12.5px;font-weight:600;opacity:0;transition:all .25s;z-index:999;pointer-events:none;display:flex;align-items:center;gap:7px;box-shadow:var(--shadow);white-space:nowrap}}
.toast.show{{opacity:1;transform:translateX(-50%) translateY(0)}}
.toast.ok{{border-color:rgba(31,184,126,.35);background:var(--green-bg);color:var(--green-t)}}

.qr-modal{{display:none;position:fixed;inset:0;background:rgba(0,0,0,.72);z-index:600;align-items:center;justify-content:center;backdrop-filter:blur(6px);padding:20px}}
.qr-modal.open{{display:flex}}
.qr-box{{background:var(--card);border:1px solid var(--card-b);border-radius:22px;padding:26px;text-align:center;max-width:340px;width:100%;box-shadow:var(--shadow)}}
.qr-title{{font-size:13.5px;font-weight:800;margin-bottom:16px;color:var(--t1)}}
.qr-img{{border-radius:14px;overflow:hidden;margin-bottom:15px}}
.qr-img img{{width:100%;display:block;background:#fff;padding:10px;border-radius:14px}}

.footer{{text-align:center;padding-top:28px;font-size:10.5px;color:var(--t3)}}
.footer a{{color:var(--accent2);font-weight:700}}

@media(max-width:520px){{
  .stats-bar{{grid-template-columns:1fr 1fr}}
  .stats-bar .stat-card:nth-child(3){{grid-column:1/-1}}
  .sub-name{{font-size:19px}}
  .copy-all-bar{{flex-direction:column;align-items:stretch}}
  .copy-all-btn{{justify-content:center}}
  .wrap{{padding:16px 12px 50px}}
  .lock-banner{{padding:32px 22px 22px}}
  .lock-form{{padding:20px 22px 26px}}
}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}

/* ══════ Classic dark refinement ══════ */
html,body{{font-family:'IBM Plex Sans',system-ui,sans-serif;-webkit-font-smoothing:antialiased;line-height:1.5}}
.sub-sub-url,.cfg-vless{{font-family:'IBM Plex Mono',ui-monospace,monospace}}
:focus-visible{{outline:2px solid var(--accent);outline-offset:2px}}
.bg-fx,.grid-fx,.sub-info::before,.cfg-tear::before,.cfg-tear::after,.lock-shield::after{{display:none}}
.dot{{animation:none}}
.brand-name{{font-size:16px;font-weight:600;letter-spacing:0}}
.brand-sub{{font-size:11.5px}}
.brand{{align-items:baseline}}
.icon-btn{{border-radius:4px;width:34px;height:34px}}
.sub-info,.stat-card,.cfg-card,.lock-card,.qr-box,.copy-all-bar,.toast{{background:var(--card);background-image:none;border:1px solid var(--card-b);border-radius:6px;box-shadow:none}}
.stat-card:hover,.cfg-card:hover{{transform:none;box-shadow:none;border-color:var(--card-bh)}}
.sub-eyebrow{{text-transform:none;letter-spacing:0;font-size:12.5px;font-weight:500;color:var(--t2)}}
.sub-name{{font-size:22px;font-weight:600;letter-spacing:0}}
.sub-desc{{font-size:13px}}
.sub-sub-box{{background:var(--bg3);border-radius:4px}}
.sub-sub-url{{color:var(--accent2)}}
.stat-label{{text-transform:none;letter-spacing:0;font-size:12px;font-weight:500;color:var(--t2)}}
.stat-val{{font-size:20px;font-weight:600;letter-spacing:0}}
.stat-card{{border-radius:6px}}
.copy-all-title{{color:var(--t1);font-weight:600}}
.copy-all-sub{{color:var(--t2)}}
.copy-all-btn{{background:var(--accent-s);color:#fff;border-radius:4px;font-weight:600}}
.copy-all-btn:hover{{transform:none;box-shadow:none;background:#4a7fe6}}
.copy-all-btn:active{{transform:none}}
.cfg-title{{text-transform:none;letter-spacing:0;font-size:14px;font-weight:600;color:var(--t1)}}
.cfg-title i{{color:var(--t3)}}
.cfg-tear{{border-top:1px solid var(--card-b);margin:0}}
.cfg-label{{font-weight:600}}
.proto-chip,.cfg-status,.conn-chip{{border-radius:3px;font-weight:600;font-size:11px}}
.pc-xhttp{{background:var(--purple-bg);color:var(--t2)}}
.ubar{{border-radius:2px;background:var(--bg3)}}
.ubar-f{{border-radius:2px}}
.cfg-link-toggle{{border:1px solid var(--card-b);border-radius:4px;background:transparent}}
.cfg-vless{{background:var(--input);border-radius:4px;color:var(--accent2)}}
.btn{{border-radius:4px;font-weight:500;font-size:12.5px}}
.btn-p{{background:var(--accent-s);box-shadow:none;color:#fff;border:1px solid transparent;font-weight:600}}
.btn-p:hover{{background:#4a7fe6}}
.btn-g,.btn-pur{{background:var(--bg3);color:var(--t1);border:1px solid var(--card-b)}}
.btn-g:hover,.btn-pur:hover{{background:var(--bg3);border-color:var(--card-bh)}}
.lock-banner{{background:none;border-bottom:1px solid var(--card-b)}}
.lock-shield{{border-radius:6px;background:var(--bg3);border:1px solid var(--card-b)}}
.lock-title{{font-weight:600;letter-spacing:0}}
.lock-inp{{background:var(--input);border-radius:4px;font-size:14px}}
.lock-btn{{border-radius:4px}}
.qr-modal{{backdrop-filter:none;background:rgba(0,0,0,.65)}}
.qr-img,.qr-img img{{border-radius:4px}}
</style>
</head>
<body>
<div class="bg-fx"></div><div class="grid-fx"></div>
<div class="toast" id="toast"></div>
<div class="qr-modal" id="qr-modal" onclick="this.classList.remove('open')">
  <div class="qr-box" onclick="event.stopPropagation()">
    <div class="qr-title" id="qr-label">QR Code</div>
    <div class="qr-img"><img id="qr-img" src="" alt="QR"></div>
    <button class="btn btn-g" style="width:100%;justify-content:center" onclick="document.getElementById('qr-modal').classList.remove('open')"><i class="ti ti-x"></i> Close</button>
  </div>
</div>
<div class="wrap">
  <div class="top">
    <div class="brand">
      <div><div class="brand-name">Panel</div><div class="brand-sub">v9.8</div></div>
    </div>
    <div class="top-actions">
      <button class="icon-btn" id="theme-toggle" onclick="toggleTheme()" title="Toggle theme"><i class="ti ti-sun" id="theme-icon"></i></button>
      
    </div>
  </div>
  <div id="root">
    <div class="empty-state"><i class="ti ti-loader-2" style="animation:spin 1s linear infinite"></i>Loading...</div>
  </div>
  <div class="footer">Panel v9.8</div>
</div>
<script>
const UUID_KEY='{uuid_key}';
let savedPw='';

let isDark=localStorage.getItem('x4g-pub-theme')!=='light';
function applyTheme(dark){{
  document.documentElement.setAttribute('data-theme',dark?'dark':'light');
  document.getElementById('theme-icon').className='ti '+(dark?'ti-sun':'ti-moon');
}}
function toggleTheme(){{isDark=!isDark;localStorage.setItem('x4g-pub-theme',isDark?'dark':'light');applyTheme(isDark)}}
applyTheme(isDark);

function toast(msg,type=''){{
  const t=document.getElementById('toast');
  t.textContent=msg;t.className='toast show'+(type?' '+type:'');
  setTimeout(()=>t.classList.remove('show'),2400);
}}
function esc(s){{return String(s||'').replace(/[&<>"']/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]))}}
function fmtB(b){{if(!b||b===0)return '0 B';if(b<1024)return b+' B';if(b<1024**2)return (b/1024).toFixed(1)+' KB';if(b<1024**3)return (b/1024**2).toFixed(2)+' MB';return (b/1024**3).toFixed(2)+' GB'}}
function fmtNum(n){{return String(n)}}
function protoChip(p){{
  if(p&&p.startsWith('xhttp'))return '<span class="proto-chip pc-xhttp"><i class="ti ti-bolt"></i> XHTTP · auto</span>';
  return '<span class="proto-chip pc-ws">VLESS · WS</span>';
}}

function showQR(label,link){{
  document.getElementById('qr-label').textContent=label;
  document.getElementById('qr-img').src='https://api.qrserver.com/v1/create-qr-code/?size=260x260&data='+encodeURIComponent(link);
  document.getElementById('qr-modal').classList.add('open');
}}

function toggleLink(i){{
  const wrap=document.getElementById('vw-'+i);
  const btn=document.getElementById('vt-'+i);
  const open=wrap.classList.toggle('open');
  btn.classList.toggle('open',open);
  btn.querySelector('.ltl span').textContent = open ? 'Hide link' : 'Show config link';
}}

async function loadData(pw=''){{
  const url='/api/public/sub/'+UUID_KEY+(pw?'?pw='+encodeURIComponent(pw):'');
  const r=await fetch(url);
  return r.json();
}}

function renderLock(name,errMsg=''){{
  document.getElementById('root').innerHTML=`
    <div class="lock-stage">
      <div class="lock-card">
        <div class="lock-banner">
          <div class="lock-shield"><i class="ti ti-shield-lock"></i></div>
          <div class="lock-title">${{esc(name)}}</div>
          <div class="lock-sub">This group is password protected. Enter the password to view the configs.</div>
        </div>
        <div class="lock-form">
          <div class="lock-err" id="lock-err">${{errMsg ? '<i class="ti ti-alert-circle"></i> '+esc(errMsg) : ''}}</div>
          <div class="lock-field">
            <i class="ti ti-lock lock-lockicon"></i>
            <input class="lock-inp" type="password" id="lock-pw" placeholder="••••••••" autofocus>
            <button class="lock-eye" type="button" onclick="togglePwVis()"><i class="ti ti-eye" id="lock-eye-icon"></i></button>
          </div>
          <button class="btn btn-p lock-btn" onclick="submitLock()"><i class="ti ti-lock-open"></i> Enter group</button>
        </div>
        <div class="lock-footer"><i class="ti ti-shield-check"></i> Your connection is encrypted</div>
      </div>
    </div>
  `;
  const inp=document.getElementById('lock-pw');
  inp.addEventListener('keydown',e=>{{if(e.key==='Enter')submitLock()}});
}}

function togglePwVis(){{
  const inp=document.getElementById('lock-pw');
  const icon=document.getElementById('lock-eye-icon');
  const toText = inp.type==='password';
  inp.type = toText ? 'text' : 'password';
  icon.className = 'ti '+(toText ? 'ti-eye-off' : 'ti-eye');
}}

async function submitLock(){{
  const pw=document.getElementById('lock-pw').value;
  const data=await loadData(pw);
  if(data.locked){{renderLock(data.name,'Incorrect password');return}}
  savedPw=pw;
  renderContent(data);
}}

function renderContent(d){{
  const activeCount=d.links.filter(l=>l.active).length;
  const baseSubUrl = d.sub_url || (window.location.protocol + '//' + window.location.host + '/p/' + UUID_KEY);
  const subUrl = baseSubUrl;

  window._x4gSubUrl  = subUrl;
  window._x4gSubName = d.name;
  window._x4gLinks   = d.links.map(l => ({{
    vless : l.vless_link,
    sub   : l.sub_url,
    label : l.label,
  }}));

  document.getElementById('root').innerHTML=`
    <div class="sub-info">
      <div class="sub-eyebrow"><i class="ti ti-folders"></i> Access group</div>
      <div class="sub-name">${{esc(d.name)}}</div>
      ${{d.desc ? `<div class="sub-desc">${{esc(d.desc)}}</div>` : ''}}
      <div class="sub-meta-row"><i class="ti ti-clock"></i> Last updated: ${{new Date().toLocaleTimeString('en-US')}}</div>
      <div class="sub-sub-box">
        <span class="sub-sub-url">${{esc(subUrl)}}</span>
        <button class="btn btn-pur" style="padding:7px 12px;font-size:10.5px"
          onclick="navigator.clipboard.writeText(window._x4gSubUrl).then(()=>toast('Sub link copied ✓','ok'))">
          <i class="ti ti-copy"></i> Copy sub link
        </button>
        <button class="btn btn-g" style="padding:7px 12px;font-size:10.5px"
          onclick="showQR(window._x4gSubName + ' — entire group', window._x4gSubUrl)">
          <i class="ti ti-qrcode"></i> QR (all)
        </button>
      </div>
    </div>

    <div class="copy-all-bar">
      <div class="copy-all-text">
        <div class="copy-all-title"><i class="ti ti-copy"></i> Copy all configs</div>
        <div class="copy-all-sub">Copy all active links in this group at once</div>
      </div>
      <button class="copy-all-btn" onclick="copyAllConfigs()"><i class="ti ti-clipboard-copy"></i> Copy all (${{fmtNum(activeCount)}})</button>
    </div>

    <div class="stats-bar">
      <div class="stat-card">
        <div class="stat-label">Active configs</div>
        <div class="stat-val">${{fmtNum(activeCount)}}</div>
        <div class="stat-sub">of ${{fmtNum(d.links.length)}} configs</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Live connections</div>
        <div class="stat-val">${{fmtNum(d.active_connections)}}</div>
        <div class="stat-sub" style="color:var(--green-t);display:flex;align-items:center;gap:4px"><span class="dot"></span> Online</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Total usage</div>
        <div class="stat-val" style="font-size:17px;margin-top:3px">${{esc(d.total_used_fmt)}}</div>
        <div class="stat-sub">All configs</div>
      </div>
    </div>

    <div class="cfg-title"><i class="ti ti-link"></i> Configs (${{fmtNum(d.links.length)}} total)</div>
    <div class="cfg-grid">
      ${{d.links.map((l, i) => {{
        const pct = l.limit_bytes === 0 ? 0 : Math.min(100, l.used_bytes / l.limit_bytes * 100);
        const bc  = pct > 90 ? 'var(--red)' : pct > 70 ? 'var(--amber)' : 'var(--green)';
        const lim = l.limit_bytes === 0 ? '∞' : fmtB(l.limit_bytes);
        return `
          <div class="cfg-card${{l.active ? '' : ' inactive'}}">
            <div class="cfg-top">
              <div class="cfg-head">
                <div>
                  <div class="cfg-label">${{esc(l.label)}}</div>
                  <div class="cfg-badges">
                    ${{protoChip(l.protocol)}}
                    ${{l.connections > 0 ? `<span class="conn-chip"><span class="dot"></span> ${{fmtNum(l.connections)}} Connect</span>` : ''}}
                  </div>
                </div>
                <span class="cfg-status ${{l.active ? 'ok' : 'no'}}">${{l.active ? '<i class="ti ti-circle-check"></i> Active' : '<i class="ti ti-circle-x"></i> Inactive'}}</span>
              </div>
              <div class="cfg-usage">
                <div class="ubar"><div class="ubar-f" style="width:${{pct}}%;background:${{bc}}"></div></div>
                <div class="utxt"><span>${{esc(l.used_fmt)}} used</span><span>Quota: ${{lim}}</span></div>
              </div>
            </div>
            <div class="cfg-tear"></div>
            <div class="cfg-bottom">
              <button class="cfg-link-toggle" id="vt-${{i}}" onclick="toggleLink(${{i}})">
                <span class="ltl"><i class="ti ti-eye"></i> <span>Show config link</span></span>
                <i class="ti ti-chevron-down"></i>
              </button>
              <div class="cfg-vless-wrap" id="vw-${{i}}">
                <div class="cfg-vless-inner">
                  <div class="cfg-vless">${{esc(l.vless_link)}}</div>
                </div>
              </div>
              <div class="cfg-actions">
                <button class="btn btn-p"
                  onclick="navigator.clipboard.writeText(window._x4gLinks[${{i}}].vless).then(()=>toast('Link copied ✓','ok'))">
                  <i class="ti ti-copy"></i> Copy link
                </button>
                <button class="btn btn-g"
                  onclick="showQR(window._x4gLinks[${{i}}].label, window._x4gLinks[${{i}}].vless)">
                  <i class="ti ti-qrcode"></i> QR
                </button>
              </div>
            </div>
          </div>
        `;
      }}).join('')}}
    </div>
  `;
  setTimeout(() => autoRefresh(), 30000);
}}

function copyAllConfigs(){{
  const links=window._x4gLinks||[];
  if(!links.length){{toast('No configs to copy','');return}}
  const text=links.map(l=>l.vless).join('\\n');
  navigator.clipboard.writeText(text).then(()=>toast('All '+fmtNum(links.length)+' configs copied ✓','ok'));
}}

async function autoRefresh(){{
  try{{
    const data = await loadData(savedPw);
    if (!data.locked) renderContent(data);
  }} catch(e) {{}}
}}

async function init(){{
  try{{
    const data = await loadData();
    if (data.locked) {{ renderLock(data.name); return; }}
    renderContent(data);
  }} catch(e) {{
    document.getElementById('root').innerHTML =
      '<div class="empty-state" style="color:var(--red-t)"><i class="ti ti-alert-circle"></i>Failed to load</div>';
  }}
}}

init();
</script>
</body></html>"""
