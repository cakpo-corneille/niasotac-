import { Link } from 'react-router-dom';
import { ShoppingBag, MapPin, Phone, Mail } from 'lucide-react';
import { useSiteSettings } from '@/hooks/useSiteSettings';

export const Footer = () => {
  const { data: settings } = useSiteSettings();
  
  return (
    <footer className="bg-card border-t border-border mt-auto">
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="space-y-4">
            <div className="flex items-center space-x-2">
              <ShoppingBag className="h-8 w-8 text-primary" />
              <span className="text-lg font-bold">
                NIASOTAC <span className="text-primary">TECH</span>
              </span>
            </div>
            <p className="text-sm text-muted-foreground">
              {settings?.company_description || 'Votre revendeur tech de confiance au Bénin. Produits de qualité à prix compétitifs.'}
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="font-semibold mb-4">Liens Rapides</h3>
            <ul className="space-y-2">
              <li>
                <Link to="/products" className="text-sm text-muted-foreground hover:text-primary transition-colors">
                  Produits
                </Link>
              </li>
              <li>
                <Link to="/services" className="text-sm text-muted-foreground hover:text-primary transition-colors">
                  Services
                </Link>
              </li>
              <li>
                <Link to="/contact" className="text-sm text-muted-foreground hover:text-primary transition-colors">
                  Contactez-nous
                </Link>
              </li>
            </ul>
          </div>

          {/* Categories */}
          <div>
            <h3 className="font-semibold mb-4">Catégories</h3>
            <ul className="space-y-2">
              <li>
                <Link to="/products?category=computers" className="text-sm text-muted-foreground hover:text-primary transition-colors">
                  Ordinateurs
                </Link>
              </li>
              <li>
                <Link to="/products?category=components" className="text-sm text-muted-foreground hover:text-primary transition-colors">
                  Composants
                </Link>
              </li>
              <li>
                <Link to="/products?category=printers" className="text-sm text-muted-foreground hover:text-primary transition-colors">
                  Imprimantes
                </Link>
              </li>
              <li>
                <Link to="/products?category=accessories" className="text-sm text-muted-foreground hover:text-primary transition-colors">
                  Accessoires
                </Link>
              </li>
            </ul>
          </div>

          {/* Contact Info */}
          <div>
            <h3 className="font-semibold mb-4">Contact</h3>
            <ul className="space-y-3">
              <li className="flex items-start space-x-2 text-sm text-muted-foreground">
                <MapPin className="h-4 w-4 mt-0.5 flex-shrink-0" />
                <span>{settings?.contact_address || 'Cotonou, Bénin'}</span>
              </li>
              <li className="flex items-center space-x-2 text-sm text-muted-foreground">
                <Phone className="h-4 w-4 flex-shrink-0" />
                <a href={`tel:${settings?.contact_phone || '+22900000000'}`} className="hover:text-primary transition-colors">
                  {settings?.contact_phone || '+229 00 00 00 00'}
                </a>
              </li>
              <li className="flex items-center space-x-2 text-sm text-muted-foreground">
                <Mail className="h-4 w-4 flex-shrink-0" />
                <a href={`mailto:${settings?.contact_email || 'contact@niasotac.com'}`} className="hover:text-primary transition-colors">
                  {settings?.contact_email || 'contact@niasotac.com'}
                </a>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-border mt-8 pt-8 text-center text-sm text-muted-foreground">
          <p>&copy; {new Date().getFullYear()} NIASOTAC TECHNOLOGIE. Tous droits réservés.</p>
        </div>
      </div>
    </footer>
  );
};
