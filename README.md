# DATA 333 Final Project - RepShare

Final Project Gradio App for DATA 333 

Group Members: **Ben Klimala**, **Liam Dale**, **Suvir Grewal**, **Daniel Zimmer**

## ✔️TODO:

- [ ] Combine Daniel and Liam's codebase into one application, provide tab functionality to switch between modes.
- [ ] Add exporting functionality to workout set creator.
  - [ ] Export as CSV / Excel functionality.
  - [ ] Export as Website functionality.
- [ ] Add saving functionality to workout recorder. >[CSV]<
- [ ] Add saving functionality to workout set creator. >[CSV]<
- [ ] Add function to save CSV / CSV locations to an SQLite database.
- [ ] Add a linear regression model which can take in data and create a graph showing when you can lift x weight at y time.
- [ ] Add searching UI allowing the display of a CSV / Dataframe.
  - [ ] Add backend code to allow querying of SQL database to populate dropdowns and search box.
  - [ ] Add in a nice display for queried recorded workouts / saved workout sets.

## 📜 Specification for application

### 🧰 What are the functions of the program?

#### ⚙️Core Functionality

- Record a daily / current workout with weight amounts.
  - **Workout** - **Sets** - **Reps**
- Create workout sets using pre-defined exercises from workout categories.
  - **Workout Section** - **Workout** - **Sets** - **Reps**
- Export created workouts to:
  - Excel Sheet / CSV
  - Website <- *stretch goal*

#### 🔧 Extra Functionality

- Generate a predictive model for weight lifting using a linear regression model
  - How much weight can I lift in X amount of days?
- Search recorded workouts which displays to screen within Gradio.
  - Save recorded workouts to SQL database in CSV format.
- Search created workout sets which displays to screen within Gradio and provides export capabilities.
  - Save created workout sets to SQL database in CSV format.

### 📚 What are the components (libraries) that need to exist?

- 🪟 Gradio 
  - Allows UI to function.
- 🐼 Pandas 
  - Necessary for working with dataframes and CSV files.
- 🪶 SQLite
  - Allows creation of searchable database for workouts / workout sets.

---

## 😴 Specification from DATA 333 Canvas

You will design and build a simple but meaningful interactive Python app that demonstrates your understanding of user-centered design, basic programming, and GUI development using Gradio (or other GUI frameworks we've covered).

This final project is your opportunity to show creativity, problem-solving, and technical implementation—all in one!
Requirements

1. Functional GUI

2. 4-5 functions using modeling, databases, loops and data structures. 

3. Stable performance.

Short Presentation (6–8 minutes)

Record a short video (screen + voice) or give a live presentation covering:

- Your app idea and the problem it solves

- Target users and scenarios

- A live walkthrough/demo of your app

- Explanation of how your logic works

- Any challenges you faced and how you solved them

- Every group member should participate in this presentation
