import tkinter as tk
from tkinter import messagebox, font
from tkinter import Canvas

class RoundedButton(tk.Canvas):
    def __init__(self, parent, text="", command=None, bg_color="#1f1f1f", text_color="white", **kwargs):
        super().__init__(parent, **kwargs)
        self.command = command
        self.configure(bg=parent["bg"], highlightthickness=0, width=250, height=50)
        self.bind("<Button-1>", lambda e: self.command() if self.command else None)
        self.bind("<Enter>", lambda e: self.on_hover())
        self.bind("<Leave>", lambda e: self.on_leave())
        self.bg_color = bg_color
        self.text_color = text_color
        self.text = text
        self.is_hovered = False
        self.draw_button()
    
    def draw_button(self):
        self.delete("all")
        color = "#333333" if self.is_hovered else self.bg_color
        self.create_oval(0, 0, 50, 50, fill=color, outline=color)
        self.create_rectangle(25, 0, 225, 50, fill=color, outline=color)
        self.create_oval(200, 0, 250, 50, fill=color, outline=color)
        self.create_text(125, 25, text=self.text, fill=self.text_color, font=("Arial", 12, "bold"))
    def on_hover(self):
        self.is_hovered = True
        self.draw_button()
    def on_leave(self):
        self.is_hovered = False
        self.draw_button()
class JobMatchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("JobMatch - Test Center")
        self.root.geometry("700x700")
        self.root.configure(bg="#ffffff")
        # Fonts to make it cool
        self.title_font = font.Font(family="Arial", size=40, weight="bold")
        self.subtitle_font = font.Font(family="Arial", size=14)
        self.text_font = font.Font(family="Arial", size=12)
        self.button_font = font.Font(family="Arial", size=11, weight="bold")
        self.job = None
        self.name = ""
        self.state = "start"
        self.selected_job = None
        self.current_question = 0
        self.score = 0
        # Job descriptions wooahhhhhhhhhhh
        self.jobs = {
            1: ("MANAGER", [
                "- Leadership and decision-making skills required",
                "- Handle stress and manage teams",
                "- Strong academic background helpful",
                "- Excellent communication skills needed"
            ]),
            2: ("DOCTOR", [
                "- Rigorous academic training (Medical degree required)",
                "- Must handle high-pressure situations calmly",
                "- Strong problem-solving and analytical skills",
                "- Compassion and patience with patients required"
            ]),
            3: ("POLICE OFFICER", [
                "- Physical fitness and discipline required",
                "- Must follow rules and guidelines strictly",
                "- Good communication skills essential",
                "- Ability to handle stressful situations"
            ]),
            4: ("ACCOUNTANT", [
                "- Strong mathematical and analytical skills",
                "- Attention to detail is crucial",
                "- Ability to organize and manage data",
                "- Patience with precise work required"
            ]),
            5: ("TEACHER", [
                "- Patience and communication skills essential",
                "- Passion for helping others learn",
                "- Structured schedule and routine preferred",
                "- Ability to explain concepts clearly"
            ]),
            6: ("ENGINEER", [
                "- Strong problem-solving and analytical skills",
                "- Technical knowledge and continuous learning",
                "- Attention to detail and precision",
                "- Ability to work with complex systems"
            ]),
            7: ("LAWYER", [
                "- Excellent communication and persuasion skills",
                "- Legal education and licensing required",
                "- Strong research and writing abilities",
                "- Ability to think critically and debate"
            ]),
            8: ("ARTIST/DESIGNER", [
                "- Creative thinking and imagination essential",
                "- Technical skills in design tools",
                "- Ability to express ideas visually",
                "- Open to feedback and willing to iterate"
            ]),
            9: ("NURSE", [
                "- Compassion and patience with patients",
                "- Medical training and certification required",
                "- Strong communication and teamwork skills",
                "- Ability to remain calm under pressure"
            ]),
            10: ("ENTREPRENEUR", [
                "- Risk-taking and innovative thinking",
                "- Business acumen and financial understanding",
                "- Leadership and decision-making skills",
                "- Resilience and adaptability essential"
            ]),
            11: ("PHARMACIST", [
                "- Extensive healthcare and pharmacology knowledge",
                "- Attention to detail and accuracy in medication dispensing",
                "- Strong patient communication and empathy",
                "- Ability to work under pressure and manage multiple tasks"
            ]),
            12: ("RECEPTIONIST", [
                "- Excellent customer service and communication skills",
                "- Organizational and multitasking abilities",
                "- Professional demeanor and problem-solving",
                "- Ability to handle administrative tasks efficiently"
            ]),
            13: ("SECURITY GUARD", [
                "- Vigilance and attention to detail",
                "- Physical fitness and ability to remain alert",
                "- Good judgment and decision-making under pressure",
                "- Strong sense of responsibility and integrity"
            ])
        }
        # Job tests questions
        self.job_tests = {
            1: ("MANAGER", [  # leadership questions
                ("How do you handle team conflicts?", ["Avoid them", "Address them directly", "Let others handle it", "Ignore them"], 1),
                ("What's most important for a leader?", ["Popularity", "Results", "Comfort", "Following rules"], 1),
                ("How do you make tough decisions?", ["By consensus", "Based on data", "Emotionally", "Randomly"], 1),
                ("What's your approach to stress?", ["Avoid it", "Manage it", "Embrace it", "Ignore it"], 1),
                ("How do you motivate a demotivated team member?", ["Ignore them", "Understand their concerns and provide support", "Give them more work", "Threaten them"], 1),
                ("What do you do when you realize you made a wrong decision?", ["Hide it", "Admit it and correct it", "Blame others", "Pretend nothing happened"], 1),
                ("How often should you give feedback to your team?", ["Never", "Once a year", "Regularly", "Only when there's a problem"], 2),
                ("What's your priority in budgeting?", ["Cut costs only", "Balance resources and goals", "Spend all funds", "No planning needed"], 1)
            ]),
            2: ("DOCTOR", [  # medical knowledge questions
                ("What does 'BP' stand for in medical terms?", ["Blood Pressure", "Body Pain", "Brain Power", "Bone Problem"], 0),
                ("How many bones are in the human body?", ["206", "208", "210", "212"], 0),
                ("What is the normal body temperature?", ["96°F", "98.6°F", "100°F", "102°F"], 1),
                ("What does CPR stand for?", ["Cardiac Pulmonary Resuscitation", "Central Patient Recovery", "Clinical Practice Rules", "Critical Patient Response"], 0),
                ("What are the main symptoms of diabetes?", ["Increased thirst, frequent urination, fatigue", "Only weight loss", "Fever", "Cough"], 0),
                ("What is a typical resting heart rate for adults?", ["40-100 bpm", "150-200 bpm", "20-50 bpm", "200+ bpm"], 0),
                ("What should you do if a patient is allergic to penicillin?", ["Give it anyway", "Use alternative antibiotics", "Skip antibiotics", "Increase the dose"], 1),
                ("What is the purpose of a physical examination?", ["Unnecessary routine", "Assess overall health and detect problems", "Waste of time", "Only for sick patients"], 1)
            ]),
            3: ("POLICE OFFICER", [  # law enforcement questions
                ("What should you do if you witness a crime?", ["Run away", "Call emergency services", "Confront the criminal", "Film it"], 1),
                ("What does 'MIRANDA' rights include?", ["Right to remain silent", "Right to a lawyer", "Both A and B", "Neither"], 2),
                ("When can police search your vehicle?", ["Anytime", "With a warrant", "If they suspect something", "Never"], 1),
                ("What should you do during a traffic stop?", ["Argue with the officer", "Stay calm and follow instructions", "Record everything", "Drive away"], 1),
                ("What is community policing?", ["Enforcement only", "Building relationships with the community", "Avoiding neighborhoods", "Ignoring complaints"], 1),
                ("How should you approach a potentially dangerous situation?", ["Rush in immediately", "Request backup and assess safety", "Send someone else", "Ignore it"], 1),
                ("What is the purpose of a police badge?", ["Fashion", "Authority and identification", "Collectible", "Optional"], 1),
                ("How do you handle a false accusation from a citizen?", ["Get angry", "Listen, investigate fairly, and clear your name if innocent", "Ignore it", "Retaliate"], 1)
            ]),
            4: ("ACCOUNTANT", [  # financial questions
                ("What is a balance sheet?", ["Income statement", "Asset/liability statement", "Cash flow statement", "Tax return"], 1),
                ("What does ROI stand for?", ["Return on Investment", "Rate of Interest", "Record of Income", "Revenue of Investment"], 0),
                ("What is depreciation?", ["Asset value increase", "Asset value decrease over time", "Tax deduction", "Profit sharing"], 1),
                ("What is a ledger?", ["Financial record book", "Legal document", "Bank statement", "Invoice"], 0),
                ("What does the equity section of a balance sheet represent?", ["Debts only", "Assets only", "Owner's stake in the business", "Monthly expenses"], 2),
                ("What is the difference between revenue and profit?", ["They're the same", "Revenue is income; profit is income minus expenses", "Profit comes first", "Revenue is larger"], 1),
                ("What is an audit?", ["A type of salary", "Examination of financial records for accuracy", "A department", "A punishment"], 1),
                ("What does GAAP stand for?", ["General Available Accounting Procedures", "Generally Accepted Accounting Principles", "Global Accounting Audit Program", "Growth and Profit"], 1)
            ]),
            5: ("TEACHER", [  # education questions
                ("What is differentiated instruction?", ["Same lesson for all", "Tailoring teaching to student needs", "Strict discipline", "Group work only"], 1),
                ("What does IEP stand for?", ["Individualized Education Program", "International Education Plan", "Institute of Educational Psychology", "Interactive Education Platform"], 0),
                ("How should you handle a disruptive student?", ["Ignore them", "Send to principal immediately", "Address the behavior calmly", "Punish severely"], 2),
                ("What is formative assessment?", ["Final exam", "Ongoing evaluation during learning", "Standardized test", "Homework grade"], 1),
                ("What is Bloom's Taxonomy used for?", ["Classroom decoration", "Organizing learning objectives", "Grading only", "Student behavior"], 1),
                ("How do you engage a shy student in class?", ["Force them to participate", "Create safe opportunities to contribute", "Ignore their silence", "Lower their grade"], 1),
                ("What is scaffolding in education?", ["Building structures", "Breaking down complex concepts into manageable steps", "Strict teaching", "Memorization"], 1),
                ("How should you communicate with parents about their child's progress?", ["Only negative feedback", "Regular, balanced, and respectful communication", "Never communicate", "Only positive feedback"], 1)
            ]),
            6: ("ENGINEER", [  # technical questions
                ("What does CAD stand for?", ["Computer Aided Design", "Central Air Duct", "Computer Application Development", "Critical Analysis Data"], 0),
                ("What is the first step in engineering design?", ["Build prototype", "Define the problem", "Test solution", "Write report"], 1),
                ("What is iteration in engineering?", ["Repeating the process", "Final step", "Documentation", "Presentation"], 0),
                ("What is a Gantt chart used for?", ["Project scheduling", "Financial planning", "Quality control", "Risk assessment"], 0),
                ("What is the purpose of a prototype?", ["Waste of resources", "Test design before full production", "Decoration", "Optional step"], 1),
                ("What does STEM stand for?", ["Science, Technology, Entertainment, Math", "Science, Technology, Engineering, Math", "Software, Tools, Engineering, Math", "System, Tools, Engineering, Management"], 1),
                ("What is root cause analysis?", ["Finding problems superficially", "Identifying the underlying reason for issues", "Blaming someone", "Quick fixes"], 1),
                ("What is a load tolerance in engineering?", ["Maximum weight something can handle", "Time limit", "Cost limit", "Safety requirement only"], 0)
            ]),
            7: ("LAWYER", [  # legal questions
                ("What does 'due process' mean?", ["Fair treatment under law", "Quick judgment", "Guilty until proven innocent", "No rights"], 0),
                ("What is precedent in law?", ["New case", "Previous court decision", "Legal opinion", "Statute"], 1),
                ("What does 'pro bono' mean?", ["For profit", "For the public good (free)", "Professional bonus", "Prolonged case"], 1),
                ("What is discovery in litigation?", ["Court verdict", "Exchange of information", "Opening statement", "Closing argument"], 1),
                ("What does 'plaintiff' refer to?", ["The defendant", "The person bringing the lawsuit", "The judge", "The jury"], 1),
                ("What is a subpoena?", ["A type of evidence", "A legal order to appear or produce evidence", "A lawyer", "A fine"], 1),
                ("What does 'contract breach' mean?", ["Starting a contract", "Breaking the terms of a contract", "Renewing a contract", "Canceling a contract"], 1),
                ("What is intellectual property?", ["Physical property", "Creations of the mind like patents and copyrights", "Mental health", "Ideas only"], 1)
            ]),
            8: ("ARTIST/DESIGNER", [  # creative questions
                ("What is the rule of thirds in design?", ["Dividing space into thirds", "Using three colors only", "Three design principles", "Three art styles"], 0),
                ("What does 'contrast' create in design?", ["Visual interest", "Boredom", "Confusion", "Harmony"], 0),
                ("What is negative space?", ["Empty space around elements", "Dark colors", "Background image", "Text space"], 0),
                ("What is typography?", ["Art of arranging type", "Painting letters", "Writing stories", "Printing books"], 0),
                ("What is color harmony?", ["Random colors", "Colors that work well together", "Only one color", "Bright colors only"], 1),
                ("What does 'balance' mean in design?", ["Symmetry only", "Visual equilibrium in composition", "Weight only", "Size only"], 1),
                ("What is a mood board used for?", ["Decoration", "Gathering inspiration and reference materials", "Final product", "Testing"], 1),
                ("What is the purpose of whitespace in design?", ["Wasted space", "Helps readability and visual focus", "Design flaw", "Must be filled"], 1)
            ]),
            9: ("NURSE", [  # healthcare questions
                ("What does 'vital signs' include?", ["Height and weight", "Blood pressure, pulse, temperature, respiration", "Blood type", "Medical history"], 1),
                ("What is HIPAA?", ["Health Insurance", "Patient privacy law", "Medical billing code", "Nursing certification"], 1),
                ("What does 'PRN' mean in medication?", ["As needed", "Every day", "With food", "Before bed"], 0),
                ("What is triage?", ["Sorting patients by urgency", "Medical billing", "Patient discharge", "Surgery scheduling"], 0),
                ("What should a nurse do if they make a medication error?", ["Hide it", "Report it immediately to ensure patient safety", "Blame the doctor", "Continue the shift normally"], 1),
                ("What is the importance of hand hygiene in nursing?", ["Unimportant", "Prevents infection transmission", "Optional", "Only before eating"], 1),
                ("How should you communicate with an anxious patient?", ["Ignore their feelings", "Listen, reassure, and provide clear information", "Use medical jargon", "Be dismissive"], 1),
                ("What is catheter care in nursing?", ["Ignoring the procedure", "Proper cleaning and maintenance to prevent infection", "Never checking it", "Change weekly always"], 1)
            ]),
            10: ("ENTREPRENEUR", [  # business questions
                ("What is a business plan?", ["Roadmap for business", "Legal document", "Tax form", "Employee handbook"], 0),
                ("What does 'ROI' measure?", ["Return on investment", "Risk of investment", "Rate of inflation", "Revenue of industry"], 0),
                ("What is market research?", ["Studying competitors and customers", "Selling products", "Making advertisements", "Hiring employees"], 0),
                ("What is a startup's burn rate?", ["Money spent per month", "Growth rate", "Failure rate", "Success rate"], 0),
                ("What is a business pivot?", ["A dance move", "Changing business strategy based on market feedback", "Quitting the business", "Moving locations"], 1),
                ("What does 'scalability' mean in business?", ["Growing staff only", "Ability to grow without proportional cost increases", "Staying small", "Size limits"], 1),
                ("What is venture capital?", ["Capital invested in cars", "Funding from investors for high-growth businesses", "Personal savings", "Bank loans only"], 1),
                ("What should you do if your startup fails?", ["Quit business entirely", "Learn from it and potentially start again", "Blame others", "Never try again"], 1)
            ]),
            11: ("PHARMACIST", [  # pharmacy questions
                ("You have to give 5 different pills to 5 different people. The pills look very similar. What should you do?", ["Double-check the prescription of the patients and the pill bottle before handing them out.", "Hand them out randomly", "Ask someone else to do it for you because you're not sure", "Give them out and apologize later."], 0),
                ("A patient asks you if it's okay to take pills that are not in their prescription. What should you do?", ["Tell them that it's probably fine.", "Ignore it because it's their choice.", "Review patient medication to ensure safety.", "Take away the pills immediately."], 2),
                ("A patient looks confused after you gave them their medication instructions. What should you do?", ["Give them a written sheet and tell them to bring it home.", "Say 'You'll figure it out yourself' and walk away.", "Make your voice louder so that they can hear you.", "Repeat the instructions slowly with simple words and ask them to explain it back."], 3),
                ("An old patient is nervous to take a new medication. What should you do?", ["Tell them, 'Don't worry, it's safe' without explaining.", "Calmly tell them why they need the medication and what to expect", "Tell them to call someone else if they're scared.", "Give them the medication and leave."], 1),
                ("A doctor's treatment order looks unusual regarding the patient's symptoms. What should you do?", ["Call the doctor to double-check the medication before giving it.", "Modify the treatment yourself.", "Give it anyway because the doctor wrote it.", "Flip a coin to decide."], 0),
                ("You see a coworker skip a safety step when preparing a patient's treatment. What should you do?", ["Ignore it because it's not your responsibility.", "Report it to your supervisor immediately.", "Confront the coworker aggressively about it.", "Follow the safety step yourself and say nothing."], 1),
                ("A patient is taking multiple medications that may interact with each other. What should you do?", ["Tell the patient to stop taking all medications.", "Review the patient's medication list for potential interactions and consult with the doctor if necessary.", "Ignore it because it's not your problem.", "Give them a pamphlet about drug interactions."], 1),
                ("A new safety warning comes out about a common type of treatment. What should you do?", ["A. Wait until your boss/supervisor informs you about it.", "B. Read the healthcare news daily and update only yourself.", "C. Ignore it because it's only a common type of treatment.", "D. Read the healthcare news daily and update your coworkers."], 3),
                ("You realize you accidentally gave the wrong medication to a patient. What should you do?", ["A. Throw away the evidence and say nothing.", "B. Immediately report it to your supervisor and check on the patient.", "C. Go to the patient yourself and change the medication to the right one.", "D. Pay with money to fix your mistake."], 1)
            ]),
            12: ("RECEPTIONIST", [  # receptionist questions
                ("1. A visitor walks into the building looking lost. What should you do?", ["A. Wait for them to come to you.", "B. Warmly welcome the visitor and ask them what they are here for.", "C. Lead them to a sign-in sheet without saying anything.", "D. Let someone else go to the visitor."], 1),
                ("2. A confused visitor calls you to ask where a specific area is located.", ["A. Provide them with a map as well as guide them with a step-by-step route for the area.", "B. Let someone else guide the visitor.", "C. Tell them to find it themselves", "D. Hand them a map of the building."], 0),
                ("3. Two staff members ask you to book appointments in the same meeting room for the same time.", ["A. Book it for the first person who asks.", "B. Choose a different date for both meetings yourself.", "C. Check the calendar and offer alternative dates/times for both.", "D. Let them decide."], 2),
                ("4. A visitor is angry because they’ve been waiting for 30 minutes. What should you do?", ["A. Calmly apologize, explain the delay, and offer another staff member for assistance.", "B. Ignore them until they stop complaining.", "C. Tell them to calm down and find another coworker to deal with them.", "D. Yell at the visitor to calm down."], 0),
                ("5. You have three tasks: answer an email, print a document, and greet a visitor. What is the best order?", ["A. Do all three at the same time.", "B. Finish the email, print the document, and then greet the visitor.", "C. Print the document first, greet the visitor, and then finish the email.", "D. Greet the visitor first, print the document. And then finish the email."], 3),
                ("6. A coworker asks you to send an email to remind all staff about a meeting. What should you do?", ["A. Type a quick email and send it to all staff.", "B. Ask someone else to do it because you don’t know how to send an email.", "C. Write the reminder on sticky notes and paste them on everyone’s desk", "D. Announce it out loud in the office."], 0),
                ("7. You need to keep track of everyone who enters the building for safety reasons. What should you do?", ["A. Try to remember everyone who enters.", "B. Don’t bother to do it because it’s only extra work.", "C. Let someone else do this work.", "D. Put a visitor log-in book and ask every visitor to sign in."], 3),
                ("8. You see a list of visitor names and phone numbers left on the counter. What should you do?", ["A. Keep them in a locked drawer or shred it if no longer needed.", "B. Call the phone numbers to give them back", "C. Leave it there, someone will pick it up.", "D. Throw it in a trash can"], 0)
            ]),
            13: ("Security Guard", [  # security questions
                ("1. You see something move while watching over CCTV feeds. What should you do?", ["A. Ignore it because it's probably nothing.", "B. Check the surrounding premises immediately.", "C. Rewind the footage and then check the surrounding premises.", "D. Call for backup."], 1),
                ("2. It's your time to patrol the area. What should you do while patrolling?", ["A. Check every area for anything unusual.", "B. Scroll through your phone while patrolling the area.", "C. Walk quickly to finish the patrol.", "D. Only check the important areas."], 0),
                ("3. Someone without a badge tries to enter an authorized personnel-only door. What should you do?", ["A. Ignore it because it's not your problem.", "B. Let them in because they probably forgot their badge.", "C. Yell at them to get out of there.", "D. Call for backup."], 3),
                ("4. You hear a loud crash and a scream from a closed office after work hours. What should you do first?", ["A. Run into the office alone immediately to see what happened.", "B. Leave the building and go home.", "C. Call for backup and wait for them before going into the office.", "D. Call for backup as you carefully go to the office."], 3),
                ("5. You see a coworker take a small item from the lost-and-found box and put it in their pocket, what should you do?", ["A. Say nothing since it's just a small thing.", "B. Ask the coworker if it's theirs first, and then listen to their explanation.", "C. Immediately report them to your supervisor.", "D. Ask your coworker to give it to you."], 1),
                ("6. A fire alarm goes off, but you don't see any smoke or fire. What should you do?", ["A. Assume it's a false alarm and turn it off.", "B. Search the area for any fire yourself.", "C. Evacuate the area according to emergency procedures.", "D. Ignore it because there’s no smoke."], 2),
                ("7. You find a door unlocked that should be locked. What should you do after securing it?", ["A. Tell your coworker about it.", "B. Do nothing because someone probably forgot to lock it.", "C. Write a short report immediately.", "D. Check the CCTV and then write a short report."], 3),
                ("8. A visitor asks you for directions to a specific floor. What should you do?", ["A. Politely give clear directions.", "B. Say “I don't know” and turn away.", "C. Point vaguely and say “over there”.", "D. Ask why they need to go there first."], 0)
            ])
        }
        # The app itself
        self.show_start_screen()
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    def show_start_screen(self):
        self.clear_window()
        self.state = "start"
        # top spacing
        top_spacer = tk.Frame(self.root, bg="#ffffff", height=40)
        top_spacer.pack()
        # logo area(placeholder)
        logo_frame = tk.Frame(self.root, bg="#ffffff")
        logo_frame.pack(pady=10)
        logo_label = tk.Label(logo_frame, text="🔗", font=("Arial", 50), bg="#ffffff")
        logo_label.pack()
        # main title
        title = tk.Label(self.root, text="JobMatch", font=self.title_font, bg="#ffffff", fg="#1f1f1f")
        title.pack(pady=20)
        # subtitle
        subtitle = tk.Label(self.root, text="Are you capable of passing the test?", font=("Arial", 14), bg="#ffffff", fg="#666666")
        subtitle.pack(pady=10)
        # name input section
        name_label = tk.Label(self.root, text="Enter your name:", font=self.subtitle_font, bg="#ffffff", fg="#1f1f1f")
        name_label.pack(pady=(30, 10))
        # styled name entry
        self.name_entry = tk.Entry(self.root, font=("Arial", 14), width=28, relief="solid", bd=2, fg="#1f1f1f")
        self.name_entry.pack(pady=15, padx=20)
        # spacing
        spacer = tk.Frame(self.root, bg="#ffffff", height=30)
        spacer.pack()
        # buttons frame
        btn_frame = tk.Frame(self.root, bg="#ffffff")
        btn_frame.pack(pady=10)
        test_btn = RoundedButton(btn_frame, text="Take Job Test", command=self.start_job_test,
                                bg_color="#1f1f1f", text_color="white")
        test_btn.pack(pady=15)
        mg_btn = RoundedButton(btn_frame, text="Manage Jobs", command=self.show_job_manager,
                              bg_color="#1f1f1f", text_color="white")
        mg_btn.pack(pady=15)
    def start_job_test(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Input Required", "Please enter your name!")
            return
        if any(char.isdigit() for char in name):
            messagebox.showwarning("Invalid Name", "Name cannot contain numbers. Please enter letters only.")
            return
        self.name = name
        self.show_job_selection()
    def show_job_manager(self):
        self.clear_window()
        self.state = "manage"
        hdr = tk.Label(self.root, text="Job Manager", font=self.title_font, bg="#ffffff", fg="#1f1f1f")
        hdr.pack(pady=10)
        self.job_listbox = tk.Listbox(self.root, font=self.text_font, width=40, height=10, bg="#f5f5f5", fg="#1f1f1f", relief=tk.FLAT, bd=1, highlightthickness=1, highlightcolor="#1f1f1f")
        self.job_listbox.pack(pady=10, padx=20)
        self.job_listbox.bind("<<ListboxSelect>>", self.update_job_preview)
        btn_frame = tk.Frame(self.root, bg="#ffffff")
        btn_frame.pack(pady=10)
        add_btn = tk.Button(btn_frame, text="Add Question", command=self.add_question_to_job,
                             font=self.button_font, bg="#1f1f1f", fg="white", padx=15, pady=8, relief=tk.FLAT)
        add_btn.pack(side=tk.LEFT, padx=5)
        edit_btn = tk.Button(btn_frame, text="Edit Question", command=self.edit_questions,
                              font=self.button_font, bg="#1f1f1f", fg="white", padx=15, pady=8, relief=tk.FLAT)
        edit_btn.pack(side=tk.LEFT, padx=5)
        back_btn = tk.Button(btn_frame, text="Back", command=self.show_start_screen,
                              font=self.button_font, bg="#1f1f1f", fg="white", padx=15, pady=8, relief=tk.FLAT)
        back_btn.pack(side=tk.LEFT, padx=5)
        self.job_preview = tk.Label(self.root, text="Select a job to see details.", font=self.text_font,
                                    bg="#ffffff", fg="#1f1f1f", justify="left", wraplength=550)
        self.job_preview.pack(pady=10, padx=10)
        self.refresh_job_list()
    def refresh_job_list(self):
        self.job_listbox.delete(0, tk.END)
        for job_id, (title, _) in sorted(self.jobs.items()):
            self.job_listbox.insert(tk.END, f"{job_id}: {title}")
    def update_job_preview(self, event=None):
        selection = self.job_listbox.curselection()
        if not selection:
            self.job_preview.config(text="Select a job to see details.")
            return
        index = selection[0]
        entry = self.job_listbox.get(index)
        job_id = int(entry.split(":", 1)[0])
        title, details = self.jobs[job_id]
        self.job_preview.config(text=f"{title}\n" + "\n".join(details), fg="#1f1f1f")
    def get_selected_job_id(self):
        selection = self.job_listbox.curselection()
        if not selection:
            return None
        entry = self.job_listbox.get(selection[0])
        return int(entry.split(":", 1)[0])
    def show_job_form(self, mode, job_id=None):
        if mode == "edit":
            selected = self.get_selected_job_id()
            if selected is None:
                messagebox.showwarning("Select Job", "Please select a job to edit.")
                return
            job_id = selected
        self.clear_window()
        hdr_text = "Add Job" if mode == "add" else "Edit Job"
        hdr = tk.Label(self.root, text=hdr_text, font=self.title_font, bg="#ffffff", fg="#1f1f1f")
        hdr.pack(pady=10)
        form_frame = tk.Frame(self.root, bg="#ffffff")
        form_frame.pack(pady=10)
        tk.Label(form_frame, text="Job Title:", font=self.text_font, bg="#ffffff", fg="#1f1f1f").grid(row=0, column=0, sticky="w", pady=5)
        self.jobtitleen = tk.Entry(form_frame, font=self.text_font, width=40, relief=tk.FLAT, bd=1)
        self.jobtitleen.grid(row=0, column=1, pady=5, padx=10)
        self.jobreq = []
        for i in range(4):
            tk.Label(form_frame, text=f"Requirement {i+1}:", font=self.text_font, bg="#ffffff", fg="#1f1f1f").grid(row=i+1, column=0, sticky="w", pady=5)
            entry = tk.Entry(form_frame, font=self.text_font, width=40, relief=tk.FLAT, bd=1)
            entry.grid(row=i+1, column=1, pady=5, padx=10)
            self.jobreq.append(entry)
        if mode == "edit":
            title, requirements = self.jobs[job_id]
            self.jobtitleen.insert(0, title)
            for entry, value in zip(self.jobreq, requirements):
                entry.insert(0, value)
        action_btn = tk.Button(self.root, text="Save", command=lambda: self.save_job(mode, job_id),
                               font=self.button_font, bg="#1f1f1f", fg="white", padx=20, pady=10, relief=tk.FLAT)
        action_btn.pack(pady=10)
        cancel_btn = tk.Button(self.root, text="Cancel", command=self.show_job_manager,
                                font=self.button_font, bg="#1f1f1f", fg="white", padx=20, pady=10, relief=tk.FLAT)
        cancel_btn.pack(pady=5)
    def save_job(self, mode, job_id=None):
        title = self.jobtitleen.get().strip()
        requirements = [entry.get().strip() for entry in self.jobreq if entry.get().strip()]
        if not title:
            messagebox.showwarning("Input Required", "Please enter a job title.")
            return
        if not requirements:
            messagebox.showwarning("Input Required", "Please enter at least one requirement.")
            return
        if mode == "add":
            new_id = max(self.jobs.keys(), default=0) + 1
            self.jobs[new_id] = (title, requirements)
        else:
            self.jobs[job_id] = (title, requirements)
        messagebox.showinfo("Saved", "Job saved successfully.")
        self.show_job_manager()
    def show_question_form(self, job_id):
        self.clear_window()
        hdr = tk.Label(self.root, text="Edit Questions", font=self.title_font, bg="#ffffff", fg="#1f1f1f")
        hdr.pack(pady=10)
        # Get current questions
        job_title, questions = self.job_tests[job_id]
        # Use a text box to edit all questions as text
        text_area = tk.Text(self.root, font=self.text_font, width=80, height=20, wrap=tk.WORD)
        text_area.pack(pady=10, padx=20)
        # Format the questions into text
        content = f"Job: {job_title}\n\n"
        for i, (q, opts, corr) in enumerate(questions, 1):
            content += f"Question {i}: {q}\n"
            for j, opt in enumerate(opts):
                content += f"  {chr(65+j)}. {opt}\n"
            content += f"Correct: {chr(65+corr)}\n\n"
        text_area.insert(tk.END, content)
        # Save button
        save_btn = tk.Button(self.root, text="Save", command=lambda: self.save_questions(job_id, text_area),
                             font=self.button_font, bg="#1f1f1f", fg="white", padx=20, pady=10, relief=tk.FLAT)
        save_btn.pack(pady=10)
        cancel_btn = tk.Button(self.root, text="Cancel", command=self.show_job_manager,
                               font=self.button_font, bg="#1f1f1f", fg="white", padx=20, pady=10, relief=tk.FLAT)
        cancel_btn.pack(pady=5)
    def save_questions(self, job_id, text_area):
        content = text_area.get("1.0", tk.END).strip()
        # Parse the content back to questions
        lines = content.split('\n')
        new_questions = []
        i = 0
        job_title = self.job_tests[job_id][0]  # keep the title
        while i < len(lines):
            if lines[i].startswith("Question "):
                q = lines[i].split(": ", 1)[1] if ": " in lines[i] else ""
                i += 1
                opts = []
                while i < len(lines) and lines[i].startswith("  "):
                    opt = lines[i].strip()[3:] if len(lines[i].strip()) > 3 else ""
                    opts.append(opt)
                    i += 1
                corr = 0
                if i < len(lines) and lines[i].startswith("Correct: "):
                    corr_letter = lines[i].split(": ")[1] if ": " in lines[i] else "A"
                    corr = ord(corr_letter.upper()) - ord('A')
                    i += 1
                new_questions.append((q, opts, corr))
                i += 1  # skip blank
            else:
                i += 1
        if len(new_questions) == 8:
            self.job_tests[job_id] = (job_title, new_questions)
            messagebox.showinfo("Saved", "Questions saved successfully.")
            self.show_job_manager()
        else:
            messagebox.showwarning("Error", f"Please ensure there are exactly 8 questions. Found {len(new_questions)}.")
    def show_add_question_form(self, job_id):
        self.clear_window()
        hdr = tk.Label(self.root, text="Add Question", font=self.title_font, bg="#ffffff", fg="#1f1f1f")
        hdr.pack(pady=10)
        form_frame = tk.Frame(self.root, bg="#ffffff")
        form_frame.pack(pady=10)
        # Question text
        tk.Label(form_frame, text="Question:", font=self.text_font, bg="#ffffff", fg="#1f1f1f").grid(row=0, column=0, sticky="nw", pady=5)
        self.q_text = tk.Text(form_frame, font=self.text_font, width=60, height=3, wrap=tk.WORD)
        self.q_text.grid(row=0, column=1, pady=5, padx=10)
        # Options
        self.q_options = []
        for i in range(4):
            tk.Label(form_frame, text=f"Option {chr(65+i)}:", font=self.text_font, bg="#ffffff", fg="#1f1f1f").grid(row=i+1, column=0, sticky="w", pady=5)
            entry = tk.Entry(form_frame, font=self.text_font, width=60, relief=tk.FLAT, bd=1)
            entry.grid(row=i+1, column=1, pady=5, padx=10)
            self.q_options.append(entry)
        # Correct answer
        tk.Label(form_frame, text="Correct Answer:", font=self.text_font, bg="#ffffff", fg="#1f1f1f").grid(row=5, column=0, sticky="w", pady=5)
        self.correct_var = tk.StringVar(value="0")
        correct_frame = tk.Frame(form_frame, bg="#ffffff")
        correct_frame.grid(row=5, column=1, sticky="w", padx=10)
        for i in range(4):
            tk.Radiobutton(correct_frame, text=chr(65+i), variable=self.correct_var, value=str(i), bg="#ffffff", fg="#1f1f1f").pack(side=tk.LEFT, padx=5)
        # Save and Cancel buttons
        btn_frame = tk.Frame(self.root, bg="#ffffff")
        btn_frame.pack(pady=10)
        save_btn = tk.Button(btn_frame, text="Save", command=lambda: self.save_new_question(job_id),
                             font=self.button_font, bg="#1f1f1f", fg="white", padx=20, pady=10, relief=tk.FLAT)
        save_btn.pack(side=tk.LEFT, padx=10)
        cancel_btn = tk.Button(btn_frame, text="Cancel", command=self.show_job_manager,
                               font=self.button_font, bg="#1f1f1f", fg="white", padx=20, pady=10, relief=tk.FLAT)
        cancel_btn.pack(side=tk.LEFT, padx=10)
    def save_new_question(self, job_id):
        question = self.q_text.get("1.0", tk.END).strip()
        options = [entry.get().strip() for entry in self.q_options]
        correct = int(self.correct_var.get())
        if not question:
            messagebox.showwarning("Input Required", "Please enter a question.")
            return
        if any(not opt for opt in options):
            messagebox.showwarning("Input Required", "Please enter all 4 options.")
            return
        # Add the new question to the job
        job_title, questions = self.job_tests[job_id]
        questions.append((question, options, correct))
        self.job_tests[job_id] = (job_title, questions)
        messagebox.showinfo("Saved", "Question added successfully.")
        self.show_job_manager()
    def delete_selected_job(self):
        selected = self.get_selected_job_id()
        if selected is None:
            messagebox.showwarning("Select Job", "Please select a job to delete.")
            return
        if messagebox.askyesno("Delete Job", "Are you sure you want to delete this job?"):
            self.jobs.pop(selected, None)
            self.refresh_job_list()
            self.update_job_preview()
    def edit_questions(self):
        selected = self.get_selected_job_id()
        if selected is None:
            messagebox.showwarning("Select Job", "Please select a job to edit questions.")
            return
        self.show_question_form(selected)
    def add_question_to_job(self):
        selected = self.get_selected_job_id()
        if selected is None:
            messagebox.showwarning("Select Job", "Please select a job to add a question.")
            return
        self.show_add_question_form(selected)
    #real test 
    def show_job_selection(self):
        self.clear_window()
        lbl = tk.Label(self.root, text=f"Hello {self.name}, choose a job to test for:", font=("Arial", 18, "bold"), bg="#ffffff", fg="#1f1f1f")
        lbl.pack(pady=20)
        self.job_listbox = tk.Listbox(self.root, font=self.text_font, width=40, height=10, bg="#f5f5f5", fg="#1f1f1f", relief=tk.FLAT, bd=1, highlightthickness=1, highlightcolor="#1f1f1f")
        self.job_listbox.pack(pady=10, padx=20)
        for job_id, (title, _) in sorted(self.job_tests.items()):
            self.job_listbox.insert(tk.END, f"{job_id}: {title}")
        btn_frame = tk.Frame(self.root, bg="#ffffff")
        btn_frame.pack(pady=10)
        btn = tk.Button(btn_frame, text="Take Test", command=self.begin_test,
                       font=self.button_font, bg="#1f1f1f", fg="white", padx=20, pady=10, relief=tk.FLAT)
        btn.pack(pady=10)
        back_btn = tk.Button(btn_frame, text="Back", command=self.show_start_screen,
                            font=self.button_font, bg="#1f1f1f", fg="white", padx=20, pady=10, relief=tk.FLAT)
        back_btn.pack(pady=10)
    def begin_test(self):
        selection = self.job_listbox.curselection()
        if not selection:
            messagebox.showwarning("Select Job", "Please select a job to test for.")
            return
        index = selection[0]
        entry = self.job_listbox.get(index)
        job_id = int(entry.split(":", 1)[0])
        self.selected_job = job_id
        self.current_question = 0
        self.score = 0
        self.show_test_question()
    def show_test_question(self):
        if self.current_question >= len(self.job_tests[self.selected_job][1]):
            self.show_test_result()
            return
        self.clear_window()
        job_title, questions = self.job_tests[self.selected_job]
        question, options, correct = questions[self.current_question]
        lbl = tk.Label(self.root, text=f"{job_title} Test - Question {self.current_question + 1}", font=("Arial", 18, "bold"), bg="#ffffff", fg="#1f1f1f")
        lbl.pack(pady=20)
        q_lbl = tk.Label(self.root, text=question, font=self.text_font, bg="#ffffff", fg="#1f1f1f", wraplength=550, justify="center")
        q_lbl.pack(pady=20, padx=20)
        self.option_var = tk.IntVar()
        for i, option in enumerate(options):
            rb = tk.Radiobutton(self.root, text=option, variable=self.option_var, value=i,
                               font=self.text_font, bg="#ffffff", fg="#1f1f1f", activebackground="#ffffff", activeforeground="#1f1f1f")
            rb.pack(pady=5)
        btn_frame = tk.Frame(self.root, bg="#ffffff")
        btn_frame.pack(pady=20)
        next_btn = tk.Button(btn_frame, text="Next", command=self.check_test_answer,
                            font=self.button_font, bg="#1f1f1f", fg="white", padx=20, pady=10, relief=tk.FLAT)
        next_btn.pack(side=tk.LEFT, padx=10)
    def check_test_answer(self):
        selected = self.option_var.get()
        _, questions = self.job_tests[self.selected_job]
        _, _, correct = questions[self.current_question]
        if selected == correct:
            self.score += 1
        self.current_question += 1
        self.show_test_question()
    def show_test_result(self):
        self.clear_window()
        job_title, questions = self.job_tests[self.selected_job]
        percentage = (self.score / len(questions)) * 100
        lbl = tk.Label(self.root, text="Test Results!", font=self.title_font, bg="#ffffff", fg="#1f1f1f")
        lbl.pack(pady=20)
        result_text = f"Job: {job_title}\n\n"
        # Add job description
        if self.selected_job in self.jobs:
            _, desc = self.jobs[self.selected_job]
            result_text += "Job Description:\n" + "\n".join(desc) + "\n\n"
        result_text += f"Score: {self.score}/{len(questions)} ({percentage:.1f}%)\n\n"
        if percentage >= 75:
            result_text += "Excellent! You seem well-suited for this job."
        elif percentage >= 50:
            result_text += "Good job! You have potential in this field."
        else:
            result_text += "Keep learning! This job might require more preparation."
        result_lbl = tk.Label(self.root, text=result_text, font=self.text_font, bg="#ffffff", fg="#1f1f1f", justify="center")
        result_lbl.pack(pady=20, padx=20)
        btn_frame = tk.Frame(self.root, bg="#ffffff")
        btn_frame.pack(pady=20)
        again_btn = tk.Button(btn_frame, text="Take Another Test", command=self.show_job_selection,
                             font=self.button_font, bg="#1f1f1f", fg="white", padx=15, pady=10, relief=tk.FLAT)
        again_btn.pack(side=tk.LEFT, padx=10)
        menu_btn = tk.Button(btn_frame, text="Main Menu", command=self.show_start_screen,
                            font=self.button_font, bg="#1f1f1f", fg="white", padx=15, pady=10, relief=tk.FLAT)
        menu_btn.pack(side=tk.LEFT, padx=10)
if __name__ == "__main__":
    root = tk.Tk()
    app = JobMatchApp(root)
    root.mainloop()




















































