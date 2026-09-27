# Deploying FORGE to Netlify

The site is **pure static files** — no build step, no dependencies, no server.
Netlify just serves the folder. Three ways to do it, easiest first.

---

## Option A — Drag & drop (2 minutes, no account setup beyond signup)

Best for: getting it online *right now*.

1. Download the `bootcamp` folder to your computer (or download `forge-bootcamp.zip`
   from the workspace and unzip it).
2. Go to **[app.netlify.com/drop](https://app.netlify.com/drop)**
3. Drag the **`bootcamp` folder itself** onto the drop zone.
4. Done. You get a URL like `https://spontaneous-halva-a1b2c3.netlify.app`

> **Important:** drag the folder that *contains* `index.html`. If you drag a
> parent folder, Netlify serves a directory listing instead of your site.

**Downside:** to update the site you have to re-drag the folder every time.
Fine for now, annoying later — Option B fixes that.

---

## Option B — GitHub + Netlify (recommended)

Best for: real workflow. Push a change, site updates automatically in ~20 seconds.
This is also the setup you'll use for every project in the bootcamp, so learning
it now is Week 0 practice.

### 1. Put the code on GitHub

From inside the `bootcamp` folder:

```bash
git init
git add .
git commit -m "feat: FORGE bootcamp site"
git branch -M main
```

Create an empty repo on GitHub named `forge-bootcamp` (no README, no .gitignore —
you already have both), then:

```bash
git remote add origin git@github.com:YOUR-USERNAME/forge-bootcamp.git
git push -u origin main
```

If you set up SSH keys in Week 0, the `git@` URL works. If not, use the HTTPS URL
and a personal access token as the password.

### 2. Connect Netlify

1. [app.netlify.com](https://app.netlify.com) → **Add new site** → **Import an existing project**
2. Choose **GitHub**, authorize, pick `forge-bootcamp`
3. Netlify reads `netlify.toml` and fills these in automatically:
   - **Build command:** *(empty)*
   - **Publish directory:** `.`
4. Click **Deploy**

### 3. Updating from now on

```bash
# edit curriculum source
cd _src && python3 build.py && cd ..
git add .
git commit -m "content: expand week 3 drills"
git push
```

Netlify rebuilds on every push to `main`. Pull requests get their own
**deploy preview** URL automatically — that's the professional workflow
you'll use for the rest of the program.

---

## Option C — Netlify CLI

Best for: deploying without leaving the terminal.

```bash
npm install -g netlify-cli
netlify login
cd bootcamp
netlify deploy          # draft URL, safe to test
netlify deploy --prod   # goes live
```

---

## After it's live

### Rename the site
Netlify's random name (`spontaneous-halva-a1b2c3`) is ugly.
**Site configuration → Change site name** → e.g. `forge-bootcamp`
→ gives you `https://forge-bootcamp.netlify.app`

### Custom domain
If you bought `yourname.dev` in Week 0:

1. **Domain management → Add a domain**
2. Enter your domain
3. Either point your registrar's nameservers at Netlify DNS (easiest),
   or add the DNS records Netlify shows you
4. HTTPS is automatic and free via Let's Encrypt — just wait a few minutes
   for the certificate to provision

A good setup: `forge.yourname.dev` as a subdomain, keeping the root domain
free for your portfolio site later.

### Verify the deploy

- [ ] Homepage loads, sidebar navigation works (12 groups, 67 lessons)
- [ ] Click through 3–4 lessons; code blocks, tables and exercise blocks render
- [ ] Hover a code block → the **Copy** button appears and works
- [ ] Open an exercise page → the **answer key** expands as a collapsible block
- [ ] Search finds "window function" and "idempotency"
- [ ] Mark a lesson complete, refresh — progress persists (localStorage)
- [ ] **Save backup** → downloads a `.json` file. Then **Restore** → re-imports it
- [ ] Visit `/nonexistent` → styled 404 page
- [ ] Load once, then switch your wifi off and reload → still works (service worker)
- [ ] Paste the URL into WhatsApp or LinkedIn → OG preview card appears
- [ ] Open on your phone → sidebar collapses to the ☰ button
- [ ] Add to home screen → installs as a standalone app

---

## Things that commonly go wrong

| Symptom | Cause | Fix |
|---|---|---|
| Blank page, console shows 404s on `data/*.js` | Dragged the wrong folder | Re-drag the folder containing `index.html` |
| Directory listing instead of the site | No `index.html` at publish root | Check **Publish directory** is `.` |
| Old content after pushing | Browser cache | Hard refresh (Ctrl/Cmd+Shift+R). `netlify.toml` already disables caching on `index.html` and `data/` |
| Progress reset | localStorage is **per-domain** | Expected. Progress on `localhost` won't transfer to the live URL — that is what **Save backup / Restore** is for |
| Offline mode not working | Service workers need HTTPS | Works on `localhost` and on Netlify automatically. Not on plain HTTP over a LAN IP |
| OG image not showing | Social platforms cache aggressively | Use the [Facebook debugger](https://developers.facebook.com/tools/debug/) or LinkedIn Post Inspector to force a re-scrape |
| Build fails | Netlify guessed a framework | Confirm build command is empty and publish dir is `.` |

---

## Note on privacy

This deploys **publicly**. That's usually good — it's a live artifact you can
show people, and "I built and deployed my own learning platform" is itself a
portfolio talking point.

If you'd rather keep it private:
- **Netlify password protection** (Site configuration → Access control) — paid feature
- Or keep the GitHub repo private and just run it locally with
  `python3 -m http.server 8080`
