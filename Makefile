VERSION?=$(shell cat VERSION)
SEMVER=$(shell cat VERSION)
TILT_PORT=7635
CONTEXT?=kind-us
.PHONY: up down semver tag untag

up:
	kubectx $(CONTEXT)
	mkdir -p secret
	mkdir -p config
	test -f secret/mysql.json || printf '{"host": "mysql.mysql", "user": "root", "password": "%s"}' "$$(kubectl -n mysql get secret mysql -o jsonpath='{.data.MYSQL_ROOT_PASSWORD}' | base64 -d)" > secret/mysql.json
	test -d api/ddl || (cd api; make build; make ddl;)
	tilt --port $(TILT_PORT) up

down:
	kubectx $(CONTEXT)
	tilt down

semver:
	cd api; VERSION=$(VERSION) SEMVER=$(SEMVER) make semver;
	cd gui; VERSION=$(VERSION) SEMVER=$(SEMVER) make semver;

tag:
	-git tag -a $(VERSION) -m "Version $(VERSION)"
	git push origin --tags

untag:
	-git tag -d $(VERSION)
	git push origin ":refs/tags/$(VERSION)"
