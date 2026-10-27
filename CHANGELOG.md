# Changelog

## 0.1.0

- The Cumulus app: an API and a GUI over the Cumulus terms, `Unifist`, `Unum`, `UnifistUnum`, `Entity`, `Scat`, `Flush` and `Bucket`.
- `make up` runs it locally in Tilt, GUI on http://localhost:6465 and API on http://localhost:16465.
- `make up` targets the `docker-desktop` cluster.
- The API connects the unum source as well as its own DB and writes a `Route` row in the `unum` schema when the API is built, routing this unum's data to its DB (unum-apps/cumulus#2). `config/unum.json`, the config map mounted like the secret, is the routed source's own arguments (`unum`, `local`, `members` if any), and the models still name the one source, `cumulus`. `unifist-unum` owns the `unum` schema and cumulus never migrates it.
- Jenkins names the test network and the mysql container per build, so builds of the same commit that run together don't clash (unum-apps/cumulus#4).
- Other apps can install the interface, `unum_cumulus`, from a tagged version of this repo (`setup.py` and `make setup`; Jenkins runs `make setup` on every build and, on main, tags the version with `make tag`, which does nothing if the tag is already there), as unum-apps/unifist-unum does (unum-apps/cumulus#7).
