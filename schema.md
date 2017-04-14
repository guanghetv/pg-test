# 章节
```sql

CREATE TYPE publish_state AS ENUM ('unpublished', 'published');
CREATE TYPE e_subject AS ENUM ('math', 'physics');

CREATE TABLE chapter (
  "id" serial,
  "subject" e_subject NOT NULL,
  "name" text NOT NULL,
  "state" publish_state NOT NULL,
  "order" int CONSTRAINT positive_order CHECK ("order" > 0) NOT NULL,
  "createTime" timestamptz default current_timestamp,
  _id char(24),
  PRIMARY KEY ("id")
);

CREATE INDEX "chapter_state_idx" ON  "chapter" ("state");

COMMENT ON COLUMN chapter._id IS 'ObjectId in mongodb';

```

# 主题

```sql

CREATE TYPE e_theme_icon_type AS ENUM ('perfect', 'common');

CREATE TYPE theme_icon AS (
  image varchar(200),
  svg varchar(200),
  background varchar(20),
  type e_theme_icon_type,
  goldenBackground varchar(200)
);

CREATE TABLE "theme" (
  "id" serial,
  "chapterId" int NOT NULL REFERENCES chapter(id),
  "name" text NOT NULL,
  "pay" bool NOT NULL,
  "icons" theme_icon[] NOT NULL,
  "relatedThemeId" int,
  "desc" text,
  "hasPainPoint" bool NOT NULL,
  "createTime" timestamptz default current_timestamp,
  _id char(24),
  PRIMARY KEY ("id")
);

CREATE INDEX "theme_chapter_id_idx" ON  "theme" ("chapterId");

COMMENT ON COLUMN theme._id IS 'ObjectId in mongodb';

```

# 知识点

```sql

CREATE TYPE e_pain_point AS ENUM ('big', 'small');
CREATE TYPE e_topic_type AS ENUM ('A', 'B', 'C', 'D', 'E', 'I', 'S', 'jyfs', 'dtsz', 'chapter_exam');

CREATE TABLE "topic" (
  "id" serial,
  "themeId" int NOT NULL REFERENCES theme(id),
  "name" text NOT NULL,
  "desc" text,
  "pay" bool NOT NULL,
  "type" e_topic_type NOT NULL,
  "state" publish_state NOT NULL,
  "painPoint" e_pain_point NOT NULL,
  _id char(24),
  "keyPoint" bool NOT NULL,
  PRIMARY KEY ("id")
);

CREATE INDEX ON  "topic" ("themeId");

COMMENT ON COLUMN topic._id IS 'ObjectId in mongodb';

```

# 视频
```sql

CREATE TYPE e_stage AS ENUM ('primary', 'middle', 'high');

CREATE TABLE "video" (
  "id" serial,
  "vmId" char(24) NOT NULL,
  "keywords" text,
  "name" text NOT NULL,
  "titleTime" int NOT NULL,
  "finishTime" int NOT NULL,
  duration int NOT NULL,
  subject e_subject NOT NULL,
  stage e_stage NOT NULL,
  "createTime" timestamptz default current_timestamp,
  _id char(24),
  PRIMARY KEY ("id")
);

COMMENT ON COLUMN video._id IS 'ObjectId in mongodb';

```


# 题库

```sql

CREATE TYPE problem_type AS ENUM ('single', 'multi', 'blank', 'exam');
CREATE TYPE problem_chioce AS (
  body text,
  correct bool
);

CREATE TABLE "problem" (
  "id" serial,
  "body" text NOT NULL,
  "choices" problem_chioce[],
  "type" problem_type,
  "explain" text,
  "blanks" text[],
  "prompts" text[],
  "source" text,
  difficulty int CHECK (difficulty > 0) NOT NULL,
  subject e_subject NOT NULL,
  stage e_stage NOT NULL,
  _id char(24),
  PRIMARY KEY ("id")
);

```


# 练习单元

```sql

CREATE TABLE practice (
  "id" serial,
  "name" text NOT NULL,
  subject e_subject NOT NULL,
  stage e_stage NOT NULL,
  "createTime" timestamptz default current_timestamp,
  _id char(24),
  PRIMARY KEY ("id")
);

```


# 练习与题库的多对多关系

```sql

CREATE TYPE practice_level_pool AS ENUM ('step', 'target', 'extend', 'hanger', 'exam');
CREATE TYPE practice_level_tag AS ENUM (
  'continuity',
  'noncontinuity',
  'optional',
  'variant',
  'hard',
  'hard_variant',
  'internal_migration'
);

CREATE TABLE "practiceLevel" (
  "practiceId" int REFERENCES practice(id) ON DELETE CASCADE,
  "problemId" int,
  "levelNo" int,
  "pool" practice_level_pool,
  "tags" practice_level_tag[],
  score int CHECK (score > 0) NOT NULL,
  "createTime" timestamptz,
  PRIMARY KEY ("practiceId", "problemId")
);

```


# 知识点和视频的多对多关系
```sql

CREATE TABLE "topicVideo" (
  "topicId" integer REFERENCES "topic" (id),
  "videoId" integer REFERENCES "video" (id) ON DELETE CASCADE,
  "createTime" timestamptz default current_timestamp,
  "updateTime" timestamptz NOT NULL,
  PRIMARY KEY ("topicId", "videoId")
);


-- 知识点和练习的多对多关系

CREATE TABLE "topicPractice" (
  "topicId" integer REFERENCES "topic" (id),
  "practiceId" integer REFERENCES video (id) ON DELETE CASCADE,
  "createTime" timestamptz default current_timestamp,
  "updateTime" timestamptz NOT NULL,
  PRIMARY KEY ("topicId", "practiceId")
);

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
CREATE TYPE e_role AS ENUM ( 'student', 'teacher', 'editor', 'shadow', 'customerService', 'shine' );

CREATE TABLE "user" (
  "id" uuid,
  "name" varchar(60),
  "target" varchar(20),
  "customSchool" varchar(50),
  "nickname" varchar(60),
  "password" text,
  "channel" varchar(30),
  "coins" int CHECK (coins >= 0),
  "points" int CHECK (points >= 0),
  "type" regist_type,
  "gender" e_gender,
  "email" varchar(60),
  "phone" varchar(14),
  "registTime" timestamptz,
  "from" e_from,
  "role" e_role,
  "salt" text,
  _id varchar(24),
  PRIMARY KEY ("id")
  /*CONSTRAINT proper_email CHECK (email ~* '^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$')*/
);

CREATE INDEX "user_name_idx" ON  "user" ("name");
CREATE INDEX "user_phone_idx" ON  "user" ("phone");
CREATE INDEX "user_email_idx" ON  "user" ("email");
CREATE INDEX "user_regist_time_idx" ON  "user" ("registTime");

COMMENT ON COLUMN "user".id IS 'use uuid_generate_v1mc() generate uuid!';
COMMENT ON COLUMN "user".phone IS 'include global phone number';
COMMENT ON COLUMN "user"._id IS 'ObjectId in mongodb';

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";


CREATE OR REPLACE FUNCTION user_uuid() RETURNS trigger as $user_uuid$
    BEGIN
        NEW.id := uuid_generate_v1mc();
        RETURN NEW;
    END;

$user_uuid$ LANGUAGE plpgsql;

CREATE TRIGGER emp_stamp BEFORE INSERT on "user"
    FOR EACH ROW EXECUTE PROCEDURE user_uuid();

```

因为早期数据类型控制不严格,导入数据需要临时放宽限制

```sql

alter table "user" alter COLUMN phone type varchar(99);
alter table "user" alter COLUMN email type varchar(99);
alter table "user" alter COLUMN channel type varchar(99);

-- go back
alter table "user" alter COLUMN phone type varchar(14);
alter table "user" alter COLUMN email type varchar(60);
alter table "user" alter COLUMN channel type varchar(30);

```


# dailysignins

```sql

CREATE TYPE e_aim AS ENUM ('simple', 'difficult');
CREATE TYPE user_learning_time AS (
    video float,
    practice float
);

CREATE TYPE user_abilities AS (
    _id int,
    name text,
    scores int
);


CREATE TABLE "dailySignin" (
    "userId" varchar(24) NOT NULL,
    "level" int NOT NULL,
    "nickname" text,
    "channel" text,
    "school" varchar(24),
    "customSchool" text,
    "aim" e_aim,
    "name" varchar(99),
    "type" regist_type,
    "from" e_from,
    "role" e_role,
    "email" varchar(99),
    "phone" varchar(99),
    "coins" int NOT NULL,
    "points" int NOT NULL,
    "scores" int NOT NULL,
    "region" varchar(16),
    "nation" varchar(16),
    "gender" e_gender,
    "province" varchar(16),
    "semester" text,
    "publisher" text,
    "registTime" timestamptz,
    "weekScores" int NOT NULL,
    "activateDate" timestamptz,
    "verifiedByPhone" bool,
    "vipExpirationTime" timestamptz,
    "qqOpenId" varchar(40),
    "createTime" timestamptz,
    "learningTime" jsonb NOT NULL,
    "clientType" text,
    "clientVersion" text,
    "deviceId" text,
    "userAgent" text,
    "signInDate" Date NOT NULL,
    "year" int,
    "month" int,
    "day" int,
    "hour" int,
    "weekday" int,
    "week" int,

    PRIMARY KEY ("userId", "signInDate")
);

CREATE INDEX ON  "dailySignin" ("signInDate");
CREATE INDEX ON  "dailySignin" ("level");

CREATE INDEX ON  "dailySignin" ("channel");
CREATE INDEX ON  "dailySignin" ("school");
CREATE INDEX ON  "dailySignin" ("aim");

CREATE INDEX ON  "dailySignin" ("type");
CREATE INDEX ON  "dailySignin" ("from");
CREATE INDEX ON  "dailySignin" ("role");

CREATE INDEX ON  "dailySignin" ("coins");
CREATE INDEX ON  "dailySignin" ("points");
CREATE INDEX ON  "dailySignin" ("scores");
CREATE INDEX ON  "dailySignin" ("region");
CREATE INDEX ON  "dailySignin" ("gender");

CREATE INDEX ON  "dailySignin" ("publisher", "semester");

CREATE INDEX ON  "dailySignin" ("registTime");
CREATE INDEX ON  "dailySignin" ("activateDate");
CREATE INDEX ON  "dailySignin" ("vipExpirationTime");

CREATE INDEX ON  "dailySignin" ("clientType");
CREATE INDEX ON  "dailySignin" ("clientVersion");
CREATE INDEX ON  "dailySignin" ("deviceId");
CREATE INDEX ON  "dailySignin" ("userAgent");


CREATE INDEX ON  "dailySignin" using gin (("learningTime" -> 'video'));
CREATE INDEX ON  "dailySignin" using gin (("learningTime" -> 'practice'));




```




