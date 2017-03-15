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