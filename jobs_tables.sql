-- ============================================================
-- SkillBridge — Run this entire file in the Supabase SQL Editor
-- ============================================================

-- BEFORE RUNNING:
-- 1. Go to Supabase Dashboard → Storage → New bucket
--    Name: profile-photos
--    Public: true (so profile photo URLs are accessible)
-- 2. Then run this SQL file in the SQL Editor

-- ------------------------------------------------------------
-- 1. profiles
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS profiles (
    user_id             UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    first_name          TEXT NOT NULL,
    last_name           TEXT NOT NULL,
    profile_photo_url   TEXT
);

-- ------------------------------------------------------------
-- 2. skills_list  (predefined, read-only for users)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS skills_list (
    id      SERIAL PRIMARY KEY,
    name    TEXT NOT NULL UNIQUE
);

INSERT INTO skills_list (name) VALUES
  -- Soft Skills & Professional
  ('Communication'), ('Teamwork'), ('Leadership'), ('Problem Solving'),
  ('Critical Thinking'), ('Time Management'), ('Adaptability'), ('Creativity'),
  ('Collaboration'), ('Attention to Detail'), ('Organization'), ('Multitasking'),
  ('Decision Making'), ('Conflict Resolution'), ('Mentoring'), ('Self-Motivation'),
  ('Work Ethic'), ('Dependability'), ('Flexibility'), ('Active Listening'),
  ('Empathy'), ('Patience'), ('Integrity'), ('Professionalism'), ('Initiative'),
  ('Emotional Intelligence'), ('Stress Management'), ('Goal Setting'),
  ('Cultural Awareness'), ('Persuasion'), ('Open-Mindedness'),

  -- Project & Operations Management
  ('Project Management'), ('Agile'), ('Scrum'), ('Event Planning'),
  ('Operations Management'), ('Process Improvement'), ('Strategic Planning'),
  ('Risk Management'), ('Resource Allocation'), ('Logistics'),
  ('Supply Chain Management'), ('Procurement'), ('Vendor Management'),
  ('Contract Management'), ('Business Analysis'), ('Cost Analysis'),
  ('Quality Control'), ('Inventory Management'),

  -- Research & Analysis
  ('Research'), ('Data Analysis'), ('Qualitative Research'), ('Quantitative Research'),
  ('Survey Design'), ('Statistical Analysis'), ('Report Writing'), ('Literature Review'),
  ('Critical Analysis'), ('Fact-Checking'), ('Data Collection'), ('Epidemiology'),
  ('Biostatistics'), ('Policy Analysis'), ('Market Analysis'), ('Competitor Analysis'),

  -- Writing & Communication
  ('Technical Writing'), ('Creative Writing'), ('Copywriting'), ('Editing'),
  ('Proofreading'), ('Grant Writing'), ('Academic Writing'), ('Journalism'),
  ('Public Speaking'), ('Presentation Skills'), ('Storytelling'), ('Social Media'),
  ('Business Writing'), ('Screenwriting'), ('Blog Writing'), ('Newsletter Writing'),
  ('Media Relations'), ('Speech Writing'),

  -- Business & Finance
  ('Accounting'), ('Bookkeeping'), ('Financial Analysis'), ('Budgeting'),
  ('Financial Modeling'), ('Business Development'), ('Business Strategy'),
  ('Market Research'), ('Forecasting'), ('QuickBooks'), ('SAP'),
  ('Microsoft Excel'), ('Google Sheets'), ('Tax Preparation'), ('Auditing'),
  ('Investment Analysis'), ('Accounts Payable'), ('Accounts Receivable'),
  ('Payroll'), ('Entrepreneurship'), ('Economics'), ('Business Law'),

  -- Marketing & Sales
  ('Marketing'), ('Digital Marketing'), ('Content Creation'), ('SEO'),
  ('Email Marketing'), ('Brand Management'), ('Advertising'), ('Public Relations'),
  ('Sales'), ('Customer Retention'), ('Account Management'), ('Negotiation'),
  ('CRM Software'), ('Salesforce'), ('Cold Calling'), ('Retail'),
  ('Content Marketing'), ('Social Media Marketing'), ('Influencer Marketing'),
  ('Google Analytics'), ('Facebook Ads'), ('Brand Strategy'), ('Market Segmentation'),
  ('Lead Generation'), ('Product Marketing'),

  -- Customer Service & Support
  ('Customer Service'), ('Help Desk'), ('IT Support'), ('Client Relations'),
  ('Conflict De-escalation'), ('Call Center'), ('Technical Support'),
  ('Customer Onboarding'), ('Service Recovery'),

  -- Healthcare & Sciences
  ('Patient Care'), ('Medical Terminology'), ('CPR/First Aid'), ('HIPAA Compliance'),
  ('Phlebotomy'), ('Medical Coding'), ('Clinical Research'), ('Pharmacology'),
  ('Biology'), ('Chemistry'), ('Physics'), ('Anatomy'), ('Lab Research'),
  ('Radiology'), ('Nutrition'), ('Public Health'), ('Mental Health'),
  ('Physical Therapy'), ('Occupational Therapy'), ('Dental Assisting'),
  ('Veterinary Assisting'), ('Fitness Training'), ('Nutrition Counseling'),
  ('Addiction Counseling'), ('Behavioral Health'), ('Gerontology'),
  ('Pediatric Care'), ('Telemedicine'), ('Health Education'),
  ('Microbiology'), ('Genetics'), ('Biochemistry'), ('Neuroscience'),
  ('Environmental Science'), ('Forensic Science'),

  -- Education & Training
  ('Teaching'), ('Tutoring'), ('Curriculum Development'), ('Lesson Planning'),
  ('Classroom Management'), ('Instructional Design'), ('Special Education'),
  ('Early Childhood Education'), ('Training & Development'), ('Coaching'),
  ('Online Teaching'), ('Adult Education'), ('Academic Advising'),
  ('ESL Teaching'), ('STEM Education'), ('Corporate Training'),
  ('Literacy Instruction'), ('Student Counseling'),

  -- Social Services & Nonprofit
  ('Social Work'), ('Counseling'), ('Case Management'), ('Community Outreach'),
  ('Volunteer Management'), ('Fundraising'), ('Advocacy'), ('Crisis Intervention'),
  ('Program Development'), ('Community Development'),
  ('Human Services'), ('Child Welfare'), ('Substance Abuse Counseling'),

  -- Engineering (Non-CS)
  ('AutoCAD'), ('SolidWorks'), ('Mechanical Engineering'), ('Electrical Engineering'),
  ('Civil Engineering'), ('Structural Analysis'), ('3D Modeling'), ('Circuit Design'),
  ('CAD'), ('Quality Assurance'), ('Manufacturing'), ('Chemical Engineering'),
  ('Industrial Engineering'), ('Environmental Engineering'), ('Aerospace Engineering'),
  ('Biomedical Engineering'), ('Urban Planning'), ('Architecture'),
  ('GIS'), ('Surveying'), ('Transportation Engineering'),

  -- Arts, Media & Design
  ('Graphic Design'), ('UI/UX Design'), ('Photography'), ('Video Production'),
  ('Film Editing'), ('Illustration'), ('Animation'), ('Interior Design'),
  ('Fashion Design'), ('Music Production'), ('Drawing'), ('Painting'),
  ('Figma'), ('Adobe XD'), ('Photoshop'), ('Illustrator'), ('Canva'),
  ('Premiere Pro'), ('After Effects'), ('Motion Graphics'), ('Typography'),
  ('Logo Design'), ('Web Design'), ('Audio Engineering'), ('Sound Design'),
  ('Game Design'), ('Voice Acting'), ('Acting'), ('Theater'), ('Dance'),
  ('UX Research'), ('Podcast Production'),

  -- Legal & Compliance
  ('Legal Research'), ('Contract Review'), ('Legal Writing'),
  ('Paralegal Studies'), ('Compliance'), ('Regulatory Affairs'),
  ('Intellectual Property'), ('Contract Drafting'), ('Mediation'),
  ('Corporate Law'), ('Immigration Law'),

  -- Sciences & Social Sciences
  ('Psychology'), ('Sociology'), ('Political Science'), ('International Relations'),
  ('Anthropology'), ('Criminal Justice'), ('Criminology'), ('Public Policy'),
  ('Geography'), ('Philosophy'), ('Marine Biology'), ('Ecology'),
  ('Geology'), ('Astronomy'), ('Materials Science'),

  -- Hospitality, Tourism & Food Service
  ('Hospitality'), ('Hotel Management'), ('Tourism'), ('Travel Planning'),
  ('Food & Beverage Management'), ('Culinary Arts'), ('Baking & Pastry'),
  ('Bartending'), ('Event Catering'), ('Front Desk Operations'),

  -- Real Estate & Property
  ('Real Estate'), ('Property Management'), ('Leasing'), ('Appraisal'),

  -- Sports, Fitness & Recreation
  ('Athletic Training'), ('Sports Management'), ('Personal Training'),
  ('Physical Education'), ('Recreation Management'), ('Yoga Instruction'),

  -- Agriculture & Environment
  ('Agriculture'), ('Horticulture'), ('Landscaping'), ('Sustainability'),
  ('Environmental Policy'), ('Conservation'), ('Farming'),

  -- Languages
  ('Spanish'), ('French'), ('Mandarin'), ('German'), ('Japanese'),
  ('American Sign Language'), ('Portuguese'), ('Arabic'),
  ('Italian'), ('Korean'), ('Russian'), ('Hindi'), ('Vietnamese'),
  ('Tagalog'), ('Hebrew'), ('Dutch'),

  -- Technology (General)
  ('Microsoft Office'), ('Google Workspace'), ('Data Entry'), ('Cybersecurity'),
  ('Networking'), ('Database Management'), ('Python'), ('JavaScript'),
  ('Java'), ('HTML'), ('CSS'), ('SQL'), ('R'), ('MATLAB'),
  ('Excel'), ('Tableau'), ('Power BI'), ('Data Visualization'),
  ('Git'), ('GitHub'), ('Linux'), ('Machine Learning'), ('Artificial Intelligence'),
  ('Cloud Computing'), ('Blockchain'), ('Mobile Development'),
  ('Software Testing'), ('Network Administration'), ('Systems Administration'),
  ('Automation'), ('Web Scraping'), ('iOS Development'), ('Android Development'),

  -- Trades & Technical
  ('Welding'), ('Carpentry'), ('Plumbing'), ('Electrical Work'),
  ('HVAC'), ('Automotive Repair'), ('Construction Management'),
  ('Masonry'), ('Roofing'), ('Flooring Installation'), ('Tiling')
ON CONFLICT (name) DO NOTHING;

-- ------------------------------------------------------------
-- 3. user_skills  (up to 15 per user, enforced in app)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS user_skills (
    id          SERIAL PRIMARY KEY,
    user_id     UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    skill_id    INTEGER NOT NULL REFERENCES skills_list(id) ON DELETE CASCADE,
    UNIQUE(user_id, skill_id)
);

-- ------------------------------------------------------------
-- 4. experience
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS experience (
    id                  SERIAL PRIMARY KEY,
    user_id             UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    employer_name       TEXT NOT NULL,
    job_title           TEXT NOT NULL,
    job_type            TEXT NOT NULL
                            CHECK (job_type IN ('Full-time','Part-time','Internship',
                                                'Contract','Freelance','Volunteer')),
    currently_working   BOOLEAN NOT NULL DEFAULT FALSE,
    start_date          DATE NOT NULL,
    end_date            DATE,
    city                TEXT NOT NULL,
    state               TEXT NOT NULL,
    description         TEXT,
    CONSTRAINT exp_desc_max CHECK (char_length(description) <= 500)
);

-- ------------------------------------------------------------
-- 5. education
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS education (
    id                  SERIAL PRIMARY KEY,
    user_id             UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    school_name         TEXT NOT NULL,
    education_level     TEXT NOT NULL
                            CHECK (education_level IN (
                                'High School/GED','Technical/Vocational',
                                'Associate''s','Bachelor''s','Master''s',
                                'Doctorate','Other')),
    currently_attending BOOLEAN NOT NULL DEFAULT FALSE,
    start_date          DATE,
    end_date            DATE,
    area_of_study       TEXT,
    description         TEXT,
    CONSTRAINT edu_desc_max CHECK (char_length(description) <= 250)
);

-- ------------------------------------------------------------
-- 6. projects
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS projects (
    id                  SERIAL PRIMARY KEY,
    user_id             UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    title               TEXT NOT NULL,
    role                TEXT,
    currently_working   BOOLEAN NOT NULL DEFAULT FALSE,
    start_date          DATE,
    end_date            DATE,
    url                 TEXT,
    description         TEXT
);

-- ------------------------------------------------------------
-- 7. social_links  (one row per user)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS social_links (
    id              SERIAL PRIMARY KEY,
    user_id         UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE UNIQUE,
    linkedin_url    TEXT,
    github_url      TEXT,
    other_url       TEXT
);
