import httpx
from datetime import datetime
from ..database import db
from ..config import settings
import logging

logger = logging.getLogger(__name__)

class CVEService:
    async def fetch_cves(self, start_index: int = 0, results_per_page: int = 100):
        async with httpx.AsyncClient() as client:
            try:
                params = {
                    "startIndex": start_index,
                    "resultsPerPage": results_per_page
                }
                response = await client.get(settings.API_BASE_URL, params=params)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                logger.error(f"Error fetching CVEs: {e}")
                raise

    async def sync_cves(self, full_refresh: bool = False):
        start_index = 0
        total_processed = 0

        while True:
            data = await self.fetch_cves(start_index)
            vulnerabilities = data.get("vulnerabilities", [])

            if not vulnerabilities:
                break

            for vuln in vulnerabilities:
                cve_data = self._process_cve_item(vuln)
                await self._store_cve(cve_data)
                total_processed += 1

            start_index += 100

        return total_processed

    def _process_cve_item(self, vulnerability):
        cve = vulnerability.get("cve", {})
        metrics = cve.get("metrics", {})
        
        return {
            "cve_id": cve.get("id"),
            "description": cve.get("descriptions", [{}])[0].get("value", ""),
            "published_date": datetime.fromisoformat(cve.get("published").replace("Z", "+00:00")),
            "last_modified_date": datetime.fromisoformat(cve.get("lastModified").replace("Z", "+00:00")),
            "base_score_v2": metrics.get("cvssMetricV2", [{}])[0].get("cvssData", {}).get("baseScore"),
            "base_score_v3": metrics.get("cvssMetricV3", [{}])[0].get("cvssData", {}).get("baseScore")
        }

    async def _store_cve(self, cve_data):
        try:
            await db.cve_collection.update_one(
                {"cve_id": cve_data["cve_id"]},
                {"$set": cve_data},
                upsert=True
            )
        except Exception as e:
            logger.error(f"Error storing CVE {cve_data['cve_id']}: {e}")
            raise