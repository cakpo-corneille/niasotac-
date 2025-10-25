/**
 * Page des produits - NIASOTAC TECHNOLOGIE
 * Affiche tous les produits avec filtres de recherche et catégories
 */
import { useState, useMemo } from 'react';
import { useSearchParams } from 'react-router-dom';
import { ProductCard } from '@/components/ProductCard';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Search, Filter, Loader2 } from 'lucide-react';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { useProducts } from '@/hooks/useProducts';
import { useCategories } from '@/hooks/useCategories';

const Products = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState(searchParams.get('category') || 'all');
  const [selectedSubcategory, setSelectedSubcategory] = useState('all');

  // Récupération des données via l'API
  const { data: categories, isLoading: categoriesLoading } = useCategories();
  const { data: products, isLoading: productsLoading } = useProducts({
    search: searchQuery || undefined,
    category: selectedCategory !== 'all' ? selectedCategory : undefined,
    subcategory: selectedSubcategory !== 'all' ? selectedSubcategory : undefined,
  });

  // Obtenir les sous-catégories de la catégorie sélectionnée
  const selectedCategoryObj = useMemo(() => {
    if (!Array.isArray(categories) || selectedCategory === 'all') return null;
    return categories.find(c => c.slug === selectedCategory);
  }, [categories, selectedCategory]);

  const subcategories = selectedCategoryObj?.subcategories || [];

  const handleCategoryChange = (value: string) => {
    setSelectedCategory(value);
    setSelectedSubcategory('all');
    if (value !== 'all') {
      setSearchParams({ category: value });
    } else {
      setSearchParams({});
    }
  };

  const clearAllFilters = () => {
    setSearchQuery('');
    setSelectedCategory('all');
    setSelectedSubcategory('all');
    setSearchParams({});
  };

  const hasActiveFilters = searchQuery || (selectedCategory !== 'all') || (selectedSubcategory !== 'all');

  return (
    <div className="flex flex-col min-h-screen">
      {/* En-tête */}
      <section className="bg-gradient-to-b from-primary/5 to-background py-12 border-b">
        <div className="container mx-auto px-4">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">Nos Produits</h1>
          <p className="text-muted-foreground text-lg max-w-2xl">
            Parcourez notre vaste collection de produits tech de qualité
          </p>
        </div>
      </section>

      <div className="container mx-auto px-4 py-8">
        {/* Filtres */}
        <div className="mb-8 space-y-4">
          <div className="flex flex-col md:flex-row gap-4">
            {/* Recherche */}
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Rechercher des produits..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10"
              />
            </div>

            {/* Filtre par catégorie */}
            <Select value={selectedCategory} onValueChange={handleCategoryChange}>
              <SelectTrigger className="w-full md:w-[220px]">
                <Filter className="h-4 w-4 mr-2" />
                <SelectValue placeholder="Toutes les catégories" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Toutes les catégories</SelectItem>
                {Array.isArray(categories) && categories.map((cat) => (
                  <SelectItem key={cat.id} value={cat.slug}>
                    {cat.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>

            {/* Filtre par sous-catégorie */}
            {selectedCategory !== 'all' && subcategories.length > 0 && (
              <Select value={selectedSubcategory} onValueChange={setSelectedSubcategory}>
                <SelectTrigger className="w-full md:w-[220px]">
                  <SelectValue placeholder="Sous-catégorie" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">Toutes les sous-catégories</SelectItem>
                  {subcategories.map((sub) => (
                    <SelectItem key={sub.id} value={sub.slug}>
                      {sub.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            )}
          </div>

          {/* Filtres actifs */}
          {hasActiveFilters && (
            <div className="flex items-center gap-2 flex-wrap">
              {selectedCategory !== 'all' && (
                <Button
                  variant="secondary"
                  size="sm"
                  onClick={() => handleCategoryChange('all')}
                >
                  {selectedCategoryObj?.name}
                  <span className="ml-2">×</span>
                </Button>
              )}
              {selectedSubcategory !== 'all' && (
                <Button
                  variant="secondary"
                  size="sm"
                  onClick={() => setSelectedSubcategory('all')}
                >
                  {subcategories.find(s => s.slug === selectedSubcategory)?.name}
                  <span className="ml-2">×</span>
                </Button>
              )}
              {searchQuery && (
                <Button
                  variant="secondary"
                  size="sm"
                  onClick={() => setSearchQuery('')}
                >
                  "{searchQuery}"
                  <span className="ml-2">×</span>
                </Button>
              )}
              <Button
                variant="ghost"
                size="sm"
                onClick={clearAllFilters}
              >
                Effacer tous les filtres
              </Button>
            </div>
          )}
        </div>

        {/* Nombre de résultats */}
        {!productsLoading && products && (
          <div className="mb-6">
            <p className="text-muted-foreground">
              {products.count} {products.count === 1 ? 'produit trouvé' : 'produits trouvés'}
            </p>
          </div>
        )}

        {/* Grille de produits */}
        {productsLoading || categoriesLoading ? (
          <div className="flex justify-center items-center py-20">
            <Loader2 className="h-12 w-12 animate-spin text-primary" />
          </div>
        ) : products && products.results && products.results.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 pb-12">
            {products.results.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        ) : (
          <div className="text-center py-20">
            <div className="max-w-md mx-auto space-y-4">
              <p className="text-muted-foreground text-lg mb-4">
                {hasActiveFilters 
                  ? 'Aucun produit ne correspond à vos critères de recherche' 
                  : 'Aucun produit disponible pour le moment'}
              </p>
              {hasActiveFilters && (
                <Button onClick={clearAllFilters}>
                  Effacer les filtres
                </Button>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Products;
