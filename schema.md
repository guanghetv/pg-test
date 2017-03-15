# 章节
```sql

CREATE TYPE publishstate AS ENUM ('unpublished', 'published');
CREATE TYPE e_subject AS ENUM ('math', 'physics');

CREATE TABLE "chapter" (
  "id" serial,
  "subject" e_subject NOT NULL,
  "name" text NOT NULL,
  "status" publishstate NOT NULL,
  "order" int CONSTRAINT positive_order CHECK ("order" > 0) NOT NULL,
  "createTime" timestamptz default current_timestamp,
  _id varchar(24),
  PRIMARY KEY ("id")
);

CREATE INDEX "chapter_status_idx" ON  "chapter" ("status");

COMMENT ON COLUMN chapter._id IS 'ObjectId in mongodb';

```

# 用户
```sql

CREATE TYPE regist_type AS ENUM (
    'signup',
    'batch',
    'qq',
    'weixin',
    'cyxt',
    'bjxxt',
    'cqxxt',
    'lnxxt',
    'ynxxt',
    'tjxxt',
    'twsm',
    'eduyun'
);

CREATE TYPE e_gender AS ENUM ('male', 'female');
CREATE TYPE e_from AS ENUM ( 'pc', 'ios', 'android', 'mobile', 'shadow');
CREATE TYPE e_role AS ENUM ( 'student', 'teacher', 'editor' );

CREATE TABLE "user" (
  "id" uuid,
  "name" varchar(60),
  "target" varchar(20),
  "customSchool" varchar(50),
  "nickname" varchar(60),
  "password" text,
  "channel" varchar(30),
  "coins" int CHECK (coins > 0),
  "points" int CHECK (points > 0),
  "type" regist_type,
  "gender" e_gender,
  "email" varchar(60),
  "phone" varchar(14),
  "registTime" timestamptz,
  "from" e_from,
  "role" e_role,
  "salt" text,
  PRIMARY KEY ("id"),
  CONSTRAINT proper_email CHECK (email ~* '^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$')
);

CREATE INDEX "user_name_idx" ON  "user" ("name");
CREATE INDEX "user_phone_idx" ON  "user" ("phone");
CREATE INDEX "user_email_idx" ON  "user" ("email");
CREATE INDEX "user_regist_time_idx" ON  "user" ("registTime");

COMMENT ON COLUMN "user".id IS 'use uuid_generate_v1mc() generate uuid!';
COMMENT ON COLUMN "user".phone IS 'include global phone number';

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

```