BEGIN;
--
-- Alter field key on apikeys
--
ALTER TABLE "app_apikeys" ADD CONSTRAINT "app_apikeys_key_428076af_uniq" UNIQUE ("key");
CREATE INDEX "app_apikeys_key_428076af_like" ON "app_apikeys" ("key" varchar_pattern_ops);
COMMIT;
