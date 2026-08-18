import { apiClient } from '@/services/apiClient';

export const nutritionApi = {
  getMealPlans: () => apiClient.get('/nutrition/meal-plans'),
  getMealPlanById: (id) => apiClient.get(`/nutrition/meal-plans/${id}`),
  create: (payload) => apiClient.post('/nutrition/meal-plans', payload),
  update: (id, payload) => apiClient.put(`/nutrition/meal-plans/${id}`, payload),
  remove: (id) => apiClient.delete(`/nutrition/meal-plans/${id}`),
};
