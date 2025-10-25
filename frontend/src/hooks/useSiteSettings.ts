import { useQuery } from '@tanstack/react-query';
import { api } from '@/lib/api';

export interface SiteSettings {
  whatsapp_number: string;
  contact_email: string;
  contact_phone: string;
  contact_address: string;
  company_name: string;
  company_description: string;
  updated_at: string;
}

export const useSiteSettings = () => {
  return useQuery<SiteSettings>({
    queryKey: ['site-settings'],
    queryFn: async () => {
      const data = await api.get('/settings/');
      return data;
    },
    staleTime: 1000 * 60 * 30,
    retry: 3,
  });
};
