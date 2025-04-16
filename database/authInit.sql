CREATE DATABASE authservice;
-- \c authservice;
-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- CREATE TABLE accounts (
--     id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
--     username VARCHAR(255) UNIQUE NOT NULL,
--     email VARCHAR(255) UNIQUE NOT NULL,
--     password TEXT NOT NULL,
--     isActive BOOLEAN DEFAULT TRUE,
--     createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     updatedAt TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
--     deletedAt TIMESTAMP DEFAULT NULL
-- );


-- CREATE TABLE password_resets (
--     id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
--     accountID UUID REFERENCES Accounts(id) ON DELETE CASCADE,
--     resetToken TEXT NOT NULL,
--     expires TIMESTAMPTZ NOT NULL,
--     createdAt TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
--     updatedAt TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
--     deletedAt TIMESTAMP DEFAULT NULL
-- );

-- CREATE TABLE login_histories (
--     id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
--     accountID UUID REFERENCES Accounts(id) ON DELETE CASCADE,
--     ipAddress INET NOT NULL,
--     userAgent TEXT,
--     loginTime TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
-- );

-- Nếu muốn mở lại bảng OAuthProviders
-- CREATE TABLE OauthProviders (
--     id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
--     accountID UUID REFERENCES Accounts(id) ON DELETE CASCADE,
--     provider VARCHAR(50) NOT NULL CHECK (provider IN ('google', 'facebook', 'github')),
--     providerID VARCHAR(255) UNIQUE NOT NULL,
--     accessToken TEXT NOT NULL,
--     refreshToken TEXT,
--     expires TIMESTAMPTZ
-- );