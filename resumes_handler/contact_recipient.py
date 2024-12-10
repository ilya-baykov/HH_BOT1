from requests_handler.requests_manager import request_manager
from resumes_handler.applicant_info import Applicant
from logger import logger


class ContactRecipient:
    def __init__(self, applicants: list[Applicant]):
        self.applicants = applicants
        self.candidates = self._bypassing_candidates()

    def _bypassing_candidates(self):
        candidates = []
        for candidate in self.applicants:
            contact_info_response = request_manager.get.get_resume(resume_id=candidate.id)
            try:
                contact_info = contact_info_response.json()
                candidate.total_experience = contact_info.get('total_experience')
                candidate.last_name = contact_info.get('last_name')
                candidate.first_name = contact_info.get('first_name')
                candidate.contact_phone = contact_info.get('contact_phone')
                candidate.sites_links = contact_info.get('sites_links')
                candidates.append(candidate)
            except Exception as e:
                logger.error(f"При попытке получить контакную информацию по кандидату - произошла ошибка:{e}")
        return candidates

    @property
    def get_candidates(self):
        return self.candidates
