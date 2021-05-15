# MinerU API Server

API server for [MinerU](https://github.com/opendatalab/MinerU).

## Quick Start

```bash
git clone https://github.com/neka-nat/mineru-api.git --recurse
cd mineru-api
docker compose up
```

## Request parsing

Use curl.

```bash
curl -X PUT http://localhost:3000/api/parse -F "file=@/path/to/file.pdf"
```

Or access `http://localhost:3000/docs` in your browser.


## ToDo

- [ ] Download images
- [ ] Utility for deploying to public cloud
