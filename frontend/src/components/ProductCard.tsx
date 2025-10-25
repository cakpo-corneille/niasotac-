import { Link } from 'react-router-dom';
import { MessageCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardFooter, CardHeader } from '@/components/ui/card';
import { Product } from '@/hooks/useProducts';

interface ProductCardProps {
  product: Product;
}

export const ProductCard = ({ product }: ProductCardProps) => {
  const formatPrice = (price: string | number) => {
    if (typeof price === 'string') {
      return `${parseFloat(price).toLocaleString('fr-FR')} FCFA`;
    }
    return `${price.toLocaleString('fr-FR')} FCFA`;
  };

  const displayPrice = product.display_price || formatPrice(product.price);

  return (
    <Card className="group overflow-hidden hover:card-shadow-hover transition-all duration-300 hover:scale-[1.02]">
      <CardHeader className="p-0">
        <Link to={`/products/${product.slug}`}>
          <div className="relative aspect-square overflow-hidden bg-secondary">
            <img
              src={product.image}
              alt={product.name}
              className="w-full h-full object-contain group-hover:scale-105 transition-transform duration-500"
              loading="lazy"
              onError={(e) => {
                const target = e.target as HTMLImageElement;
                target.src = '/placeholder.svg';
              }}
            />
            {product.featured && (
              <div className="absolute top-3 right-3 bg-accent text-accent-foreground px-3 py-1 rounded-full text-xs font-semibold">
                Vedette
              </div>
            )}
          </div>
        </Link>
      </CardHeader>
      
      <CardContent className="p-4 space-y-2">
        <Link to={`/products/${product.slug}`}>
          <h3 className="font-semibold text-lg group-hover:text-primary transition-colors line-clamp-1">
            {product.name}
          </h3>
        </Link>
        {product.brand && (
          <p className="text-xs text-muted-foreground font-medium">
            {product.brand}
          </p>
        )}
        <p className="text-sm text-muted-foreground line-clamp-2">
          {product.description}
        </p>
        <div className="pt-2">
          <span className="text-2xl font-bold text-primary">
            {displayPrice}
          </span>
        </div>
      </CardContent>
      
      <CardFooter className="p-4 pt-0 flex gap-2">
        <Link to={`/products/${product.slug}`} className="flex-1">
          <Button variant="outline" className="w-full">
            Voir détails
          </Button>
        </Link>
        <a
          href={product.whatsapp_link}
          target="_blank"
          rel="noopener noreferrer"
          className="flex-1"
        >
          <Button className="w-full bg-[#25D366] hover:bg-[#20BD5A] text-white">
            <MessageCircle className="mr-2 h-4 w-4" />
            Commander
          </Button>
        </a>
      </CardFooter>
    </Card>
  );
};
