import { HeroSection } from '@/components/HeroSection';
import { CategoryCard } from '@/components/CategoryCard';
import { ProductCard } from '@/components/ProductCard';
import { WhatsAppButton } from '@/components/WhatsAppButton';
import { Button } from '@/components/ui/button';
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from '@/components/ui/carousel';
import { Link } from 'react-router-dom';
import { ArrowRight, Shield, Truck, Headset, Loader2 } from 'lucide-react';
import { useMainCategories } from '@/hooks/useCategories';
import { useFeaturedProducts } from '@/hooks/useProducts';

const Home = () => {
  const { data: categories, isLoading: categoriesLoading } = useMainCategories();
  const { data: featuredProducts, isLoading: productsLoading } = useFeaturedProducts();

  return (
    <div className="flex flex-col min-h-screen">
      <HeroSection />
      <WhatsAppButton />

      {/* Categories Section */}
      <section className="py-16 bg-secondary/30">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Parcourir par catégorie</h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              Explorez notre large gamme de produits technologiques dans différentes catégories
            </p>
          </div>

          {categoriesLoading ? (
            <div className="flex justify-center items-center py-12">
              <Loader2 className="h-8 w-8 animate-spin text-primary" />
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
              {categories?.map((category) => (
                <CategoryCard key={category.id} category={category} />
              ))}
            </div>
          )}
        </div>
      </section>

      {/* Featured Products */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between mb-12">
            <div>
              <h2 className="text-3xl md:text-4xl font-bold mb-4">Produits vedettes</h2>
              <p className="text-muted-foreground">
                Découvrez nos produits les plus populaires et recommandés
              </p>
            </div>
            <Link to="/products">
              <Button variant="outline" className="hidden md:flex">
                Voir tout
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </Link>
          </div>

          {productsLoading ? (
            <div className="flex justify-center items-center py-12">
              <Loader2 className="h-8 w-8 animate-spin text-primary" />
            </div>
          ) : featuredProducts && featuredProducts.length > 0 ? (
            <>
              <Carousel
                opts={{
                  align: "start",
                  loop: true,
                }}
                className="w-full"
              >
                <CarouselContent>
                  {featuredProducts.map((product) => (
                    <CarouselItem key={product.id} className="md:basis-1/2 lg:basis-1/3">
                      <ProductCard product={product} />
                    </CarouselItem>
                  ))}
                </CarouselContent>
                <CarouselPrevious className="hidden md:flex" />
                <CarouselNext className="hidden md:flex" />
              </Carousel>

              <div className="text-center mt-8 md:hidden">
                <Link to="/products">
                  <Button>
                    Voir tous les produits
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </Button>
                </Link>
              </div>
            </>
          ) : (
            <div className="text-center py-12 text-muted-foreground">
              Aucun produit vedette disponible pour le moment
            </div>
          )}
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-primary/5">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="flex flex-col items-center text-center space-y-4">
              <div className="h-16 w-16 rounded-full bg-accent/10 flex items-center justify-center">
                <Shield className="h-8 w-8 text-accent" />
              </div>
              <h3 className="text-xl font-semibold">Qualité garantie</h3>
              <p className="text-muted-foreground">
                Tous nos produits sont vérifiés et proviennent de magasins partenaires de confiance
              </p>
            </div>

            <div className="flex flex-col items-center text-center space-y-4">
              <div className="h-16 w-16 rounded-full bg-accent/10 flex items-center justify-center">
                <Truck className="h-8 w-8 text-accent" />
              </div>
              <h3 className="text-xl font-semibold">Commande facile</h3>
              <p className="text-muted-foreground">
                Commandez directement via WhatsApp pour un service rapide et personnalisé
              </p>
            </div>

            <div className="flex flex-col items-center text-center space-y-4">
              <div className="h-16 w-16 rounded-full bg-accent/10 flex items-center justify-center">
                <Headset className="h-8 w-8 text-accent" />
              </div>
              <h3 className="text-xl font-semibold">Support client</h3>
              <p className="text-muted-foreground">
                Notre équipe est disponible pour répondre à toutes vos questions
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
