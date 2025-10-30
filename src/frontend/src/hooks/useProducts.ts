import { useQuery } from '@tanstack/react-query';
import { api } from '@/lib/api';

export interface Product {
  id: number;
  name: string;
  slug: string;
  description: string;
  price: string;
  display_price: string;
  brand: string;
  image: string;
  category: number;
  category_name: string;
  subcategory: number | null;
  subcategory_name: string | null;
  in_stock: boolean;
  featured: boolean;
  whatsapp_link: string;
  created_at: string;
  updated_at: string;
}

export interface ProductsResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Product[];
}

export const useProducts = (params?: {
  category?: string;
  subcategory?: string;
  brand?: string;
  in_stock?: boolean;
  featured?: boolean;
  search?: string;
}) => {
  const queryParams = new URLSearchParams();
  
  if (params?.category) queryParams.append('category', params.category);
  if (params?.subcategory) queryParams.append('subcategory', params.subcategory);
  if (params?.brand) queryParams.append('brand', params.brand);
  if (params?.in_stock !== undefined) queryParams.append('in_stock', String(params.in_stock));
  if (params?.featured !== undefined) queryParams.append('featured', String(params.featured));
  if (params?.search) queryParams.append('search', params.search);

  const queryString = queryParams.toString();
  const endpoint = `/products/${queryString ? `?${queryString}` : ''}`;

  return useQuery<ProductsResponse>({
    queryKey: ['products', params],
    queryFn: () => api.get(endpoint),
  });
};

export const useProduct = (slug: string) => {
  return useQuery<Product>({
    queryKey: ['product', slug],
    queryFn: () => api.get(`/products/${slug}/`),
    enabled: !!slug,
  });
};

export const useFeaturedProducts = () => {
  return useQuery<Product[]>({
    queryKey: ['products', 'featured'],
    queryFn: () => api.get('/products/featured/'),
  });
};

export const useRecentProducts = () => {
  return useQuery<Product[]>({
    queryKey: ['products', 'recent'],
    queryFn: () => api.get('/products/recent/'),
  });
};

export const useProductStats = () => {
  return useQuery({
    queryKey: ['products', 'stats'],
    queryFn: () => api.get('/products/stats/'),
  });
};
