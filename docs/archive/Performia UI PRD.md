# **Performia: Product Requirements Document (PRD) v1.0**

Author: Gemini & User Collaboration  
Date: September 21, 2025  
Status: Final Draft for Handoff

## **1\. Vision & Mission**

**Vision:** To create a revolutionary music creation and performance ecosystem that shatters the outdated paradigm of the Digital Audio Workstation (DAW).

**Mission:** To empower solo artists with a co-creative partner—a personalized AI band that learns their unique style, follows their lead in real-time, and removes all technical barriers, allowing them to exist in a state of pure creative flow from the first idea to the final performance.

## **2\. Target Audience & Personas**

We will address the market with a tiered product strategy, each targeting a specific user persona.

* **Persona 1: The Hobbyist (Tier 1: Performia Charts)**  
  * **Who:** Students, amateur musicians, singers.  
  * **Needs:** An accurate, fun, and easy way to learn and play along with their favorite songs. They are frustrated by the rigid, inaccurate "auto-scroll" of competitors like Ultimate Guitar.  
  * **Goal:** To feel the magic of a chart that actually listens to them.  
* **Persona 2: The Creator (Tier 2: Performia Studio)**  
  * **Who:** Singer-songwriters, home studio producers, composers.  
  * **Needs:** A way to quickly capture and build upon original ideas without getting bogged down in the technical complexity of a traditional DAW.  
  * **Goal:** To compose and arrange full songs in an intuitive, conversational workflow with an AI band that feels like a creative partner.  
* **Persona 3: The Performer (Tier 3: Performia Live)**  
  * **Who:** Professional solo artists, live streamers, advanced musicians.  
  * **Needs:** A rock-solid, low-latency, all-in-one performance rig that provides a hyper-responsive AI band and a fully integrated visual show.  
  * **Goal:** To deliver a unique, dynamic, and visually stunning performance every night, with the freedom to improvise and lead the band with their musicianship.

## **3\. Product Tiers & Monetization Strategy**

* **Tier 1: Performia Charts (Freemium)**  
  * **Offering:** The standalone "Living Chart" application.  
  * **Monetization:** Free to download and use with ads and a limit on saved/imported charts. A modest monthly/annual subscription ("Charts Pro") unlocks unlimited charts, advanced practice tools, and removes ads. This is our primary user acquisition funnel.  
* **Tier 2: Performia Studio (Subscription)**  
  * **Offering:** The full "Creator" experience. Includes all "Charts Pro" features.  
  * **Monetization:** A premium monthly/annual subscription. This is our core revenue driver.  
* **Tier 3: Performia Live (Pro License)**  
  * **Offering:** The complete professional solo performance ecosystem. Includes all "Studio" features.  
  * **Monetization:** A significant one-time purchase or a high-tier annual subscription, targeting professional users who will generate income using the software.  
* **The Upgrade Path:** The UI should be designed to create a "golden path" for users. The "Charts" app will visually tease the "Studio" features (e.g., with faded-out AI band members), prompting a natural and compelling upgrade.

## **4\. The Core Ecosystem & Features**

### **4.1. The AI Conductor & The "Song Map"**

This is the foundational technology that powers the entire ecosystem.

* **The "Song Map":** This is our proprietary data format. It is not a simple text file. It is a high-fidelity, "cadence-aware" map of a song's performance, containing precise startTime and duration values for every syllable.  
* **The AI Conductor:** This is the real-time engine that listens to a user's live performance (via their audio interface) and intelligently follows them through the Song Map. It detects the user's tempo, rhythm, and chord changes, ensuring the Teleprompter and AI Band are always in perfect sync with the human performer.

### **4.2. "Song Map" Creation (A Key Differentiator)**

* **Create from Audio:** Users can provide a YouTube link, Spotify track, or MP3. Performia's "AI Deconstructor" will analyze the track and automatically generate a new, highly accurate Song Map, complete with transcribed chords and aligned lyrics.  
* **Create from Performance:** A user can record themselves singing and playing an original song. The AI will listen, detect the structure (verses, choruses), and generate a new Song Map based on their unique performance.

### **4.3. The "Blueprint View" (The Editor)**

This is the primary interface for viewing and editing a Song Map.

* **Layout:** A clean, document-style layout that is easy to read and navigate. Chords are displayed clearly above their corresponding lyrics and will never overlap.  
* **Full "Doc-Like" Editing:** All text elements—song title, artist, section headers, chords, and lyrics—must be directly editable with a simple click.  
* **Data Sync:** All edits made in this view must be saved to the underlying songPerformanceMap data and be instantly reflected in the Teleprompter view.

### **4.4. The "Living Chart" (The Teleprompter)**

This is the core performance interface. It must be beautiful, intuitive, and flawless.

* **Three-State Lyric Coloring:** Upcoming lyrics are a dimmed gray. The active syllable is highlighted with a cyan "wipe" effect. Past (sung) lyrics change to a solid, bright white.  
* **Natural Cadence:** All animations (lyric wipe, progress bars) must be driven by the precise timing data in the Song Map, ensuring they feel human and musical, not robotic.  
* **Smooth Scrolling:** The active line must always be gently guided to the vertical center of the screen.

### **4.5. The Performia Hub (Settings & Controls)**

This is the user's command center, accessible via a gear icon in the header.

* **Layout:** A slide-out panel with an overlay that allows the user to click off to collapse.  
* **"Now Playing" Tab:**  
  * **Chord Display:** A three-mode control (Off, Names, Diagrams). When in "Diagrams" mode, the chord names in the Teleprompter are replaced by persistent, inline diagrams.  
  * **Font Size:** A granular range slider for precise control.  
  * **Musical Tools:** Transpose and Capo controls that correctly adjust the musical data and display.  
* **"Library" & "AI Band" Tabs:** These provide access to the broader ecosystem features and the upgrade path to "Studio."

## **5\. Performia Studio & The AI Band**

* **AI Personas:** The AI band is not a generic session player. It's a persistent, learning entity. Users create different AI "Bands" (e.g., their Rock Trio, their Ambient Duo), and these bands learn the user's specific playing style, groove, and musical preferences over time.  
* **Conversational Creation:** In Studio Mode, the user builds a song by talking to their AI band ("Give me a simple, funky bassline") and refining the results with conversational "Nudges" ("Play that a little behind the beat").  
* **Choreographing the Cues:** This is the critical link between Studio and Live. The user "teaches" the AI band how to perform the song by defining dynamic baselines for each section and assigning specific musical or gestural cues to transitions.

## **6\. Performia Live & The Visual Performance Engine**

* **Leading the Band:** In Live Mode, the user leads the performance with their instrument. Their playing dynamics, tempo shifts, and pre-defined musical/visual cues tell the AI Musical Director when to change sections.  
* **Hardware Integration:**  
  * **Audio I/O:** The app must have a clear settings area to select an audio interface (e.g., Presonus Quantum 2626\) and monitor input/output levels. **Low latency (sub-10ms) is a non-negotiable requirement.**  
  * **Footpedal Mapping:** A simple, drag-and-drop interface for mapping MIDI footpedals (e.g., SoftStep 3\) to **expressive controls** like "Toggle Jam Mode," "Loop Section," or triggering visual effects—NOT for changing song sections.  
* **Visual Performance Engine:** An integrated, real-time visual show.  
  * **Avatars:** Users can customize the appearance of their AI bandmates. These avatars must perform expressively, with movements perfectly synced to the music they are creating.  
  * **Generative Worlds:** The entire performance takes place in a dynamic, audio-reactive 3D environment.  
  * **AI Director:** A virtual cinematographer that creates a professional, multi-camera show in real-time, cutting between shots based on the musical performance.

This document outlines the full vision. We will begin with a flawless execution of **Tier 1: Performia Charts**, ensuring its "Living Chart" and "Blueprint View" are market-ready, while building the foundation for the "Studio" and "Live" tiers to come.