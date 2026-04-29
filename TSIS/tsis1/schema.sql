-- Drop existing tables if they exist (for clean setup)
DROP TABLE IF EXISTS phones, contacts, groups CASCADE;

-- Create groups table
CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

-- Create contacts table with all required fields
CREATE TABLE contacts (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100),
    email VARCHAR(255) UNIQUE,
    birthday DATE,
    group_id INTEGER REFERENCES groups(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create phones table for multiple phone numbers per contact
CREATE TABLE phones (
    id SERIAL PRIMARY KEY,
    contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE,
    phone VARCHAR(20) NOT NULL,
    type VARCHAR(20) CHECK (type IN ('home', 'work', 'mobile')) DEFAULT 'mobile'
);

-- Insert default groups
INSERT INTO groups (name) VALUES ('Family'), ('Work'), ('Friend'), ('Other')
ON CONFLICT (name) DO NOTHING;