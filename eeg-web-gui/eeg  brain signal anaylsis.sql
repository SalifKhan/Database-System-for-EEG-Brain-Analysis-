/*assignment no 02
grp members: Muhammad Salif Ilyas B23F000AI044
			 Muhammad Abdullah b23F0001AI006
             Husnain Sajid B23F0001AI007
             Usba Khan B23F0922AI190*/
-- Create database for EEG Brain Signal Analysis
CREATE DATABASE eeg_brain_signal_analysis;

-- Use the created database
USE eeg_brain_signal_analysis;

-- Create Researcher table (independent entity)
CREATE TABLE Researcher (
    researcher_id INT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    institution VARCHAR(100),
    department VARCHAR(100),
    specialization VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Subject table (independent entity)
CREATE TABLE Subject (
    subject_id INT PRIMARY KEY,
    name VARCHAR(100),
    age INT NOT NULL,
    gender VARCHAR(20),
    handedness VARCHAR(20),
    medical_history TEXT,
    consent_status BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Cognitive_Task table (independent entity)
CREATE TABLE Cognitive_Task (
    task_id INT PRIMARY KEY,
    task_name VARCHAR(100) NOT NULL,
    description TEXT,
    difficulty_level VARCHAR(50),
    duration_seconds INT,
    instructions TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create ML_Model table (independent entity)
CREATE TABLE ML_Model (
    model_id INT PRIMARY KEY,
    model_name VARCHAR(100) NOT NULL,
    model_type VARCHAR(50),
    framework VARCHAR(50),
    accuracy DECIMAL(5,2),
    parameters TEXT,
    creation_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create EEG_Reading table with foreign keys
CREATE TABLE EEG_Reading (
    recording_id INT PRIMARY KEY,
    researcher_id INT NOT NULL,
    subject_id INT NOT NULL,
    task_id INT NOT NULL,
    recording_date TIMESTAMP NOT NULL,
    duration_seconds INT,
    equipment_used VARCHAR(100),
    sampling_rate INT,
    channel_count INT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (researcher_id) REFERENCES Researcher(researcher_id),
    FOREIGN KEY (subject_id) REFERENCES Subject(subject_id),
    FOREIGN KEY (task_id) REFERENCES Cognitive_Task(task_id)
);

-- Create Brain_Signal table with foreign key
CREATE TABLE Brain_Signal (
    signal_id INT PRIMARY KEY,
    recording_id INT NOT NULL,
    channel_name VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    amplitude DECIMAL(10,6) NOT NULL,
    frequency DECIMAL(10,2),
    signal_quality VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (recording_id) REFERENCES EEG_Reading(recording_id)
);

-- Create Signal_Analysis table with foreign keys
CREATE TABLE Signal_Analysis (
    analysis_id INT PRIMARY KEY,
    signal_id INT NOT NULL,
    model_id INT NOT NULL,
    analysis_type VARCHAR(50) NOT NULL,
    analysis_date TIMESTAMP NOT NULL,
    features TEXT,
    results TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (signal_id) REFERENCES Brain_Signal(signal_id),
    FOREIGN KEY (model_id) REFERENCES ML_Model(model_id)
);

-- Create Signal_Processing table with foreign key
CREATE TABLE Signal_Processing (
    process_id INT PRIMARY KEY,
    signal_id INT,
    process_type VARCHAR(50),
    parameters TEXT,
    results TEXT,
    created_at TIMESTAMP,
    FOREIGN KEY (signal_id) REFERENCES Brain_Signal(signal_id)
);

-- Create EEG_Device table
CREATE TABLE EEG_Device (
    device_id INT PRIMARY KEY,
    manufacturer VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    serial_number VARCHAR(50) UNIQUE,
    specifications TEXT,
    calibration_date DATE,
    last_maintenance_date DATE,
    status VARCHAR(20) DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Experiment_Log table
CREATE TABLE Experiment_Log (
    log_id INT PRIMARY KEY,
    recording_id INT NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    event_time TIMESTAMP NOT NULL,
    description TEXT,
    severity VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (recording_id) REFERENCES EEG_Reading(recording_id)
);

-- Create Signal_Annotation table
CREATE TABLE Signal_Annotation (
    annotation_id INT PRIMARY KEY,
    signal_id INT NOT NULL,
    annotation_type VARCHAR(50) NOT NULL,
    start_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP NULL,
    description TEXT,
    confidence_score DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (signal_id) REFERENCES Brain_Signal(signal_id)
);

-- Create Research_Project table
CREATE TABLE Research_Project (
    project_id INT PRIMARY KEY,
    project_name VARCHAR(100) NOT NULL,
    description TEXT,
    start_date DATE NOT NULL,
    end_date DATE,
    status VARCHAR(20) DEFAULT 'Active',
    funding_source VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Project_Researcher table (Many-to-Many relationship)
CREATE TABLE Project_Researcher (
    project_id INT NOT NULL,
    researcher_id INT NOT NULL,
    role VARCHAR(50) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (project_id, researcher_id),
    FOREIGN KEY (project_id) REFERENCES Research_Project(project_id),
    FOREIGN KEY (researcher_id) REFERENCES Researcher(researcher_id)
);

-- Add indexes to improve query performance
CREATE INDEX idx_eeg_researcher ON EEG_Reading(researcher_id);
CREATE INDEX idx_eeg_subject ON EEG_Reading(subject_id);
CREATE INDEX idx_eeg_task ON EEG_Reading(task_id);
CREATE INDEX idx_signal_recording ON Brain_Signal(recording_id);
CREATE INDEX idx_analysis_signal ON Signal_Analysis(signal_id);
CREATE INDEX idx_analysis_model ON Signal_Analysis(model_id);

-- Insert sample researchers
INSERT INTO Researcher (researcher_id, first_name, last_name, email, institution, department, specialization)
VALUES 
(1, 'Jane', 'Smith', 'jane.smith@research.org', 'Brain Research Institute', 'Neuroscience', 'Cognitive Neuroscience'),
(2, 'John', 'Doe', 'john.doe@university.edu', 'University Medical Center', 'Neural Engineering', 'BCI Development'),
(3, 'Sarah', 'Johnson', 'sarah.j@neurolab.com', 'NeuroLab Research Center', 'Clinical Neuroscience', 'EEG Analysis');

-- Insert sample subjects
INSERT INTO Subject (subject_id, name, age, gender, handedness, medical_history, consent_status)
VALUES 
(1, 'Alex', 25, 'Male', 'Right', 'No significant medical history', TRUE),
(2, 'Maria', 30, 'Female', 'Right', 'Mild anxiety', TRUE),
(3, 'Taylor', 42, 'Non-binary', 'Left', 'Previous concussion in 2019', TRUE),
(4, 'Emily', 35, 'Female', 'Right', 'None', TRUE),
(5, 'Sam', 28, 'Male', 'Ambidextrous', 'Migraines', TRUE);

-- Insert sample cognitive tasks
INSERT INTO Cognitive_Task (task_id, task_name, description, difficulty_level, duration_seconds, instructions)
VALUES 
(1, 'N-back test', 'Working memory assessment task', 'Medium', 300, 'Press button when current stimulus matches one presented n trials ago'),
(2, 'Stroop test', 'Measures reaction time and selective attention', 'Easy', 180, 'Name the color of the word, not the word itself'),
(3, 'Mental arithmetic', 'Sequential math problems of increasing difficulty', 'Hard', 420, 'Solve the arithmetic problems as quickly and accurately as possible');

-- Insert sample ML models
INSERT INTO ML_Model (model_id, model_name, model_type, framework, accuracy, parameters, creation_date)
VALUES 
(1, 'CNNBrainNet', 'Convolutional Neural Network', 'TensorFlow', 87.50, 'Layers: 5, Neurons: 256, Dropout: 0.2', '2024-02-15'),
(2, 'EEG-LSTM', 'Long Short-Term Memory Network', 'PyTorch', 92.30, 'Units: 128, Timesteps: 50', '2024-03-20'),
(3, 'RandomForestEEG', 'Random Forest', 'Scikit-learn', 85.70, 'Trees: 500, Max depth: 10', '2024-01-10');

-- Insert sample EEG readings
INSERT INTO EEG_Reading (recording_id, researcher_id, subject_id, task_id, recording_date, duration_seconds, equipment_used, sampling_rate, channel_count, notes)
VALUES 
(1, 1, 1, 1, '2024-03-10 09:30:00', 600, 'BrainScope EEG-2000', 256, 64, 'Subject was well-rested'),
(2, 1, 2, 2, '2024-03-12 14:15:00', 450, 'BrainScope EEG-2000', 256, 64, 'Subject reported feeling slightly tired'),
(3, 2, 3, 3, '2024-03-15 10:00:00', 520, 'NeuroScan Ultra', 512, 128, 'Subject performed exceptionally well'),
(4, 2, 1, 2, '2024-03-17 11:30:00', 380, 'NeuroScan Ultra', 512, 128, 'Follow-up session'),
(5, 3, 4, 1, '2024-03-18 13:45:00', 450, 'EEGLab Pro', 1024, 256, 'High density recording');

-- Insert sample brain signals
INSERT INTO Brain_Signal (signal_id, recording_id, channel_name, timestamp, amplitude, frequency, signal_quality)
VALUES 
(1, 1, 'Fp1', '2024-03-10 09:30:05', 2.345678, 12.45, 'Excellent'),
(2, 1, 'Fp2', '2024-03-10 09:30:05', 2.123456, 11.98, 'Excellent'),
(3, 1, 'F3', '2024-03-10 09:30:05', 1.987654, 10.56, 'Good'),
(4, 2, 'Fp1', '2024-03-12 14:15:10', 2.654321, 13.22, 'Good'),
(5, 2, 'Fp2', '2024-03-12 14:15:10', 2.456789, 12.87, 'Excellent'),
(6, 3, 'Oz', '2024-03-15 10:00:15', 3.123456, 15.78, 'Excellent'),
(7, 3, 'Pz', '2024-03-15 10:00:15', 2.876543, 14.32, 'Excellent'),
(8, 4, 'C3', '2024-03-17 11:30:20', 1.765432, 9.87, 'Good'),
(9, 5, 'C4', '2024-03-18 13:45:25', 2.234567, 11.23, 'Excellent');

-- Insert sample signal analyses
INSERT INTO Signal_Analysis (analysis_id, signal_id, model_id, analysis_type, analysis_date, features, results)
VALUES 
(1, 1, 1, 'FFT Analysis', '2024-03-20 13:45:00', 'Alpha band: 9.8Hz, Beta band: 21.4Hz', 'Strong alpha rhythms detected'),
(2, 2, 1, 'Wavelet Transform', '2024-03-20 14:30:00', 'Decomposition level: 5', 'Clear cognitive response patterns'),
(3, 3, 2, 'Time-Frequency Analysis', '2024-03-22 09:15:00', 'STFT window: 256', 'Event-related oscillations detected'),
(4, 4, 2, 'Coherence Analysis', '2024-03-25 10:00:00', 'Channels: Fp1-Fp2', 'High inter-hemispheric coherence'),
(5, 6, 3, 'Power Spectral Density', '2024-03-28 15:20:00', 'Frequency bands: Delta, Theta, Alpha, Beta, Gamma', 'Increased gamma activity during task'),
(6, 8, 3, 'Independent Component Analysis', '2024-03-30 11:10:00', 'Components: 20', 'Successful artifact removal'),
(7, 9, 1, 'Event-Related Potential', '2024-04-02 14:45:00', 'Time window: -200ms to 800ms', 'P300 component clearly identified');

-- Create stored procedure to get all EEG readings for a specific subject
DELIMITER //
CREATE PROCEDURE GetSubjectEEGReadings(IN sub_id INT)
BEGIN
    SELECT r.recording_id, r.recording_date, r.duration_seconds, 
           res.first_name, res.last_name, 
           ct.task_name, ct.difficulty_level
    FROM EEG_Reading r
    JOIN Researcher res ON r.researcher_id = res.researcher_id
    JOIN Cognitive_Task ct ON r.task_id = ct.task_id
    WHERE r.subject_id = sub_id
    ORDER BY r.recording_date DESC;
END //
DELIMITER ;

-- Create stored procedure to get all brain signals for a specific EEG reading
DELIMITER //
CREATE PROCEDURE GetEEGSignals(IN rec_id INT)
BEGIN
    SELECT bs.signal_id, bs.channel_name, bs.timestamp, bs.amplitude, bs.frequency, bs.signal_quality
    FROM Brain_Signal bs
    WHERE bs.recording_id = rec_id
    ORDER BY bs.channel_name, bs.timestamp;
END //
DELIMITER ;

-- Create view for researcher productivity
CREATE VIEW ResearcherProductivity AS
SELECT 
    r.researcher_id,
    CONCAT(r.first_name, ' ', r.last_name) AS researcher_name,
    COUNT(er.recording_id) AS total_recordings,
    COUNT(DISTINCT er.subject_id) AS total_subjects,
    COUNT(DISTINCT er.task_id) AS total_tasks,
    MAX(er.recording_date) AS latest_recording
FROM 
    Researcher r
LEFT JOIN 
    EEG_Reading er ON r.researcher_id = er.researcher_id
GROUP BY 
    r.researcher_id, researcher_name;

-- Create view for model performance overview
CREATE VIEW ModelPerformance AS
SELECT 
    m.model_id,
    m.model_name,
    m.model_type,
    m.accuracy,
    COUNT(sa.analysis_id) AS times_used,
    MIN(sa.analysis_date) AS first_used,
    MAX(sa.analysis_date) AS last_used
FROM 
    ML_Model m
LEFT JOIN 
    Signal_Analysis sa ON m.model_id = sa.model_id
GROUP BY 
    m.model_id, m.model_name, m.model_type, m.accuracy;

-- Trigger for EEG_Reading validation
DELIMITER //
CREATE TRIGGER validate_eeg_reading
BEFORE INSERT ON EEG_Reading
FOR EACH ROW
BEGIN
    IF NEW.duration_seconds <= 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Duration must be positive';
    END IF;
    
    IF NEW.sampling_rate <= 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Sampling rate must be positive';
    END IF;
END //
DELIMITER ;

-- Trigger for automatic experiment logging
DELIMITER //
CREATE TRIGGER log_eeg_recording
AFTER INSERT ON EEG_Reading
FOR EACH ROW
BEGIN
    INSERT INTO Experiment_Log (recording_id, event_type, event_time, description, severity)
    VALUES (NEW.recording_id, 'Recording Started', NEW.recording_date, 
            CONCAT('New EEG recording session started for subject ', NEW.subject_id), 'Info');
END //
DELIMITER ;

-- Procedure to get researcher's project involvement
DELIMITER //
CREATE PROCEDURE GetResearcherProjects(IN res_id INT)
BEGIN
    SELECT p.project_id, p.project_name, p.description, p.status,
           pr.role, pr.start_date, pr.end_date
    FROM Research_Project p
    JOIN Project_Researcher pr ON p.project_id = pr.project_id
    WHERE pr.researcher_id = res_id
    ORDER BY p.start_date DESC;
END //
DELIMITER ;

-- Procedure to get signal statistics
DELIMITER //
CREATE PROCEDURE GetSignalStatistics(IN rec_id INT)
BEGIN
    SELECT 
        COUNT(*) as total_signals,
        AVG(amplitude) as avg_amplitude,
        MIN(amplitude) as min_amplitude,
        MAX(amplitude) as max_amplitude,
        AVG(frequency) as avg_frequency,
        COUNT(DISTINCT channel_name) as unique_channels
    FROM Brain_Signal
    WHERE recording_id = rec_id;
END //
DELIMITER ;

-- Procedure to get project performance metrics
DELIMITER //
CREATE PROCEDURE GetProjectMetrics(IN proj_id INT)
BEGIN
    SELECT 
        p.project_name,
        COUNT(DISTINCT er.subject_id) as total_subjects,
        COUNT(DISTINCT er.researcher_id) as total_researchers,
        COUNT(DISTINCT er.recording_id) as total_recordings,
        COUNT(DISTINCT sa.analysis_id) as total_analyses,
        MIN(er.recording_date) as first_recording,
        MAX(er.recording_date) as latest_recording
    FROM Research_Project p
    JOIN Project_Researcher pr ON p.project_id = pr.project_id
    JOIN EEG_Reading er ON er.researcher_id = pr.researcher_id
    LEFT JOIN Brain_Signal bs ON bs.recording_id = er.recording_id
    LEFT JOIN Signal_Analysis sa ON sa.signal_id = bs.signal_id
    WHERE p.project_id = proj_id
    GROUP BY p.project_name;
END //
DELIMITER ;

-- View for project overview
CREATE VIEW ProjectOverview AS
SELECT 
    p.project_id,
    p.project_name,
    p.status,
    p.start_date,
    p.end_date,
    COUNT(DISTINCT pr.researcher_id) as researcher_count,
    COUNT(DISTINCT er.recording_id) as recording_count,
    COUNT(DISTINCT er.subject_id) as subject_count
FROM Research_Project p
LEFT JOIN Project_Researcher pr ON p.project_id = pr.project_id
LEFT JOIN EEG_Reading er ON er.researcher_id = pr.researcher_id
GROUP BY p.project_id, p.project_name, p.status, p.start_date, p.end_date;

-- View for signal quality analysis
CREATE VIEW SignalQualityAnalysis AS
SELECT 
    er.recording_id,
    er.recording_date,
    s.subject_id,
    s.age,
    s.gender,
    bs.channel_name,
    bs.signal_quality,
    COUNT(*) as signal_count,
    AVG(bs.amplitude) as avg_amplitude
FROM EEG_Reading er
JOIN Subject s ON er.subject_id = s.subject_id
JOIN Brain_Signal bs ON er.recording_id = bs.recording_id
GROUP BY er.recording_id, er.recording_date, s.subject_id, s.age, s.gender, bs.channel_name, bs.signal_quality;

-- View for ML model performance tracking
CREATE VIEW ModelPerformanceTracking AS
SELECT 
    m.model_id,
    m.model_name,
    m.model_type,
    m.accuracy,
    COUNT(sa.analysis_id) as total_analyses,
    COUNT(DISTINCT sa.analysis_type) as analysis_types,
    MIN(sa.analysis_date) as first_use,
    MAX(sa.analysis_date) as last_use,
    AVG(CASE WHEN sa.results LIKE '%success%' THEN 1 ELSE 0 END) as success_rate
FROM ML_Model m
LEFT JOIN Signal_Analysis sa ON m.model_id = sa.model_id
GROUP BY m.model_id, m.model_name, m.model_type, m.accuracy;

-- Insert sample EEG devices
INSERT INTO EEG_Device (device_id, manufacturer, model, serial_number, specifications, calibration_date, last_maintenance_date, status)
VALUES 
(1, 'BrainScope', 'EEG-2000', 'BS2000-001', '64 channels, 256Hz sampling rate', '2024-01-15', '2024-03-01', 'Active'),
(2, 'NeuroScan', 'Ultra', 'NS-U-002', '128 channels, 512Hz sampling rate', '2024-02-01', '2024-03-15', 'Active'),
(3, 'EEGLab', 'Pro', 'ELP-003', '256 channels, 1024Hz sampling rate', '2024-01-20', '2024-03-10', 'Maintenance');

-- Insert sample research projects
INSERT INTO Research_Project (project_id, project_name, description, start_date, end_date, status, funding_source)
VALUES 
(1, 'Cognitive Load Study', 'Investigating EEG patterns during different cognitive tasks', '2024-01-01', '2024-12-31', 'Active', 'NSF'),
(2, 'BCI Development', 'Developing brain-computer interface using EEG signals', '2024-02-01', '2025-01-31', 'Active', 'DARPA'),
(3, 'Clinical EEG Analysis', 'Analyzing EEG patterns in clinical populations', '2024-03-01', '2024-09-30', 'Active', 'NIH');

-- Insert project-researcher relationships
INSERT INTO Project_Researcher (project_id, researcher_id, role, start_date)
VALUES 
(1, 1, 'Principal Investigator', '2024-01-01'),
(1, 2, 'Research Assistant', '2024-01-01'),
(2, 2, 'Lead Developer', '2024-02-01'),
(2, 3, 'Data Analyst', '2024-02-01'),
(3, 3, 'Clinical Researcher', '2024-03-01');