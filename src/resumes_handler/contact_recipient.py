from src.requests_handler.requests_manager import request_manager
from src.resumes_handler.applicant_info import Applicant
from config.logger import logger


class CandidateInfoRecipient:
    def __init__(self, applicants: list[Applicant]):
        self.applicants = applicants
        self.candidates = self._bypassing_candidates()

    def _bypassing_candidates(self):
        candidates = []
        for candidate in self.applicants:
            candidate_info_response = request_manager.get.get_resume(resume_id=candidate.id)
            try:
                candidate_info = candidate_info_response.json()
                candidate.photo_link = candidate_info.get('photo') and candidate_info['photo'].get('medium') or None

                candidate.total_experience = candidate_info.get('total_experience')
                candidate.skills = candidate_info.get('skills')
                candidates.append(candidate)
            except Exception as e:
                logger.error(f"При попытке получить детальную информацию по кандидату - произошла ошибка:{e}")
        return candidates

    @property
    def get_candidates(self):
        return self.candidates
