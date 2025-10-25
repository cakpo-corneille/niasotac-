import { useQuery } from '@tanstack/react-query';
import { api } from '@/lib/api';

export interface Subcategory {
  id: number;
  name: string;
  slug: string;
  icon: string | null;
  image: string | null;
  product_count: number;
}

export interface Category {
  id: number;
  name: string;
  slug: string;
  icon: string | null;
  image: string | null;
  parent: number | null;
  subcategories: Subcategory[];
  product_count: number;
  is_main_category: boolean;
  created_at: string;
  updated_at: string;
}

export const useCategories = () => {
  return useQuery<Category[]>({
    queryKey: ['categories'],
    queryFn: () => api.get('/categories/'),
  });
};

export const useMainCategories = () => {
  return useQuery<Category[]>({
    queryKey: ['categories', 'main'],
    queryFn: () => api.get('/categories/main_categories/'),
  });
};

export const useCategory = (slug: string) => {
  return useQuery<Category>({
    queryKey: ['category', slug],
    queryFn: () => api.get(`/categories/${slug}/`),
    enabled: !!slug,
  });
};

export const useCategoryProducts = (slug: string) => {
  return useQuery({
    queryKey: ['category', slug, 'products'],
    queryFn: () => api.get(`/categories/${slug}/products/`),
    enabled: !!slug,
  });
};
