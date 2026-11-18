# Wild Butchery

Website for @Wild Butchery, the butchery in the Bush Centre, 3883 Olifant Road, Marloth Park: steaks, boerewors and game boerewors, droëwors, biltong, sosaties, home-made crumbed products and deli gifts. Tagline from their Facebook page: "No need to bring meat."

Live: https://obsidianstudiodesigns.github.io/Wild-Butchery/

- Static HTML, CSS and JavaScript with no build step, hosted on GitHub Pages from `main`.
- Content comes from the Facebook page (facebook.com/WildButchery): address, WhatsApp 064 072 5121, phone 071 658 3316, wildbutchery@gmail.com, Afrikaans and English, and the products on their posts and posters.
- All photographs are AI-generated scene-setters (Figma, gpt-image). Swap in photos of the real counter and shopfront when available.
- `tools/build_logo.py` lifts the acacia tree out of the Facebook profile logo into a transparent PNG.
- `tools/build_assets.py` makes the WebP images, the tree mark, favicons (tree in front of an ember sun), the icon sprite and the WhatsApp/social share image (`assets/img/og-share.jpg`) from the raw files in `_source/` (not in git).
- `tools/build_pages.py` makes the privacy policy, terms, 404, robots.txt, sitemap.xml and the manifest.
- The braai planner suggests amounts (about 350 g per adult and half that per child, per braai) and opens WhatsApp to 064 072 5121 with the list filled in. There is no backend.
- Look: dusk in the bushveld. Ironwood brown, bone and dry-grass neutrals with one ember accent, ember particles drifting over the hero photo. Fonts: Big Shoulders Display (headlines, butcher-signage feel) and Figtree (body), self-hosted, OFL. Icons: Phosphor (MIT).

## To confirm with the client

- Trading hours (Facebook hides them; the site says to check Facebook for holiday hours).
- That they take pre-orders on WhatsApp for collection, as the planner and FAQ suggest.
- Which game products they stock regularly besides game boerewors and game sosaties.
- Real photos of the shop, and whether they want a custom domain.

Designed by [Obsidian Studio Designs](https://obsidianstudiodesigns.co.za/).
