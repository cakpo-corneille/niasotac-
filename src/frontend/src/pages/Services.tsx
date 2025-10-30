/**
 * Page Services - NIASOTAC TECHNOLOGIE
 * Décrit les services offerts par NIASOTAC
 */
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Camera, TrendingUp, MessageSquare, ShoppingCart, CheckCircle2, MessageCircle } from 'lucide-react';
import { Link } from 'react-router-dom';

const Services = () => {
  const whatsappNumber = '+237XXXXXXXXX';
  const whatsappMessage = encodeURIComponent('Bonjour ! J\'aimerais en savoir plus sur vos services.');

  const services = [
    {
      icon: Camera,
      title: 'Photographie de Produits',
      description: 'Nous visitons les magasins d\'électronique partenaires à travers le Bénin et prenons des photos de haute qualité de leurs produits, en capturant chaque détail de manière professionnelle.',
      benefits: [
        'Images professionnelles de produits',
        'Angles et vues multiples',
        'Photos haute résolution',
        'Délai rapide',
      ],
    },
    {
      icon: TrendingUp,
      title: 'Promotion en Ligne',
      description: 'Nous promouvons les produits via notre site web et nos réseaux sociaux, atteignant les clients qui recherchent activement des produits tech.',
      benefits: [
        'Large portée en ligne',
        'Marketing ciblé',
        'Présence sur les réseaux sociaux',
        'Référencement optimisé',
      ],
    },
    {
      icon: MessageSquare,
      title: 'Négociation des Prix',
      description: 'Nous travaillons avec nos magasins partenaires pour négocier les meilleurs prix possibles pour nos clients, vous garantissant un excellent rapport qualité-prix.',
      benefits: [
        'Prix compétitifs',
        'Remises en gros disponibles',
        'Relations directes avec les magasins',
        'Tarification transparente',
      ],
    },
    {
      icon: ShoppingCart,
      title: 'Vente Directe',
      description: 'Nous gérons l\'ensemble du processus de vente, de la demande à la livraison, vous facilitant l\'obtention des produits tech dont vous avez besoin.',
      benefits: [
        'Processus de commande simple',
        'Livraison rapide',
        'Transactions sécurisées',
        'Support WhatsApp 24/7',
      ],
    },
  ];

  return (
    <div className="flex flex-col min-h-screen">
      {/* Section Hero */}
      <section className="bg-gradient-to-b from-primary/5 to-background py-16 md:py-24 border-b">
        <div className="container mx-auto px-4">
          <div className="max-w-3xl mx-auto text-center space-y-6">
            <h1 className="text-4xl md:text-5xl font-bold">Nos Services</h1>
            <p className="text-xl text-muted-foreground">
              Nous comblons le fossé entre les magasins tech et les clients, rendant les produits 
              de qualité accessibles et abordables à travers le Bénin
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center pt-4">
              <Link to="/products">
                <Button size="lg">
                  Parcourir les Produits
                </Button>
              </Link>
              <a
                href={`https://wa.me/${whatsappNumber}?text=${whatsappMessage}`}
                target="_blank"
                rel="noopener noreferrer"
              >
                <Button size="lg" variant="outline" className="bg-[#25D366] hover:bg-[#20BD5A] text-white border-[#25D366]">
                  <MessageCircle className="mr-2 h-4 w-4" />
                  Contactez-nous
                </Button>
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* Comment Nous Fonctionnons */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Notre Processus</h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              Notre processus simplifié vous garantit les meilleurs produits aux meilleurs prix
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 max-w-6xl mx-auto">
            {[
              { step: '1', title: 'Visite des Magasins', desc: 'Nous visitons les magasins d\'électronique partenaires' },
              { step: '2', title: 'Documentation Produits', desc: 'Photos et collecte des détails produits' },
              { step: '3', title: 'Mise en Ligne', desc: 'Publication des produits sur notre site' },
              { step: '4', title: 'Connexion & Vente', desc: 'Connexion des clients avec les meilleures offres' },
            ].map((item, index) => (
              <div key={index} className="relative">
                <div className="text-center space-y-4">
                  <div className="h-16 w-16 rounded-full bg-primary text-primary-foreground text-2xl font-bold flex items-center justify-center mx-auto">
                    {item.step}
                  </div>
                  <h3 className="font-semibold text-lg">{item.title}</h3>
                  <p className="text-sm text-muted-foreground">{item.desc}</p>
                </div>
                {index < 3 && (
                  <div className="hidden lg:block absolute top-8 left-[60%] w-[80%] h-0.5 bg-border"></div>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Détails des Services */}
      <section className="py-16 bg-secondary/30">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-6xl mx-auto">
            {services.map((service, index) => (
              <Card key={index} className="hover:card-shadow-hover transition-shadow">
                <CardContent className="p-6 space-y-4">
                  <div className="h-14 w-14 rounded-lg bg-primary/10 flex items-center justify-center">
                    <service.icon className="h-7 w-7 text-primary" />
                  </div>
                  
                  <div>
                    <h3 className="text-xl font-semibold mb-2">{service.title}</h3>
                    <p className="text-muted-foreground">{service.description}</p>
                  </div>

                  <div className="space-y-2 pt-2">
                    {service.benefits.map((benefit, idx) => (
                      <div key={idx} className="flex items-start gap-2">
                        <CheckCircle2 className="h-5 w-5 text-accent flex-shrink-0 mt-0.5" />
                        <span className="text-sm">{benefit}</span>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Pourquoi Choisir NIASOTAC */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto">
            <div className="text-center mb-12">
              <h2 className="text-3xl md:text-4xl font-bold mb-4">Pourquoi Choisir NIASOTAC ?</h2>
              <p className="text-muted-foreground">
                Nous sommes bien plus qu'un simple revendeur - nous sommes votre partenaire tech de confiance
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {[
                {
                  title: 'Réseau Étendu',
                  desc: 'Nous collaborons avec plus de 50 magasins d\'électronique à travers le Bénin, vous offrant la plus large sélection de produits.',
                },
                {
                  title: 'Prix Compétitifs',
                  desc: 'Nos relations solides avec les magasins nous permettent de négocier de meilleurs prix pour vous.',
                },
                {
                  title: 'Garantie de Qualité',
                  desc: 'Chaque produit est vérifié avant d\'être répertorié, vous assurant des articles authentiques et de qualité.',
                },
                {
                  title: 'Toujours Disponible',
                  desc: 'Support 24/7 via WhatsApp, nous sommes là quand vous avez besoin d\'assistance.',
                },
              ].map((item, index) => (
                <div key={index} className="p-6 rounded-lg border bg-card space-y-2">
                  <h3 className="font-semibold text-lg">{item.title}</h3>
                  <p className="text-muted-foreground">{item.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Section CTA */}
      <section className="py-16 bg-gradient-to-r from-primary to-primary/80 text-primary-foreground">
        <div className="container mx-auto px-4">
          <div className="max-w-3xl mx-auto text-center space-y-6">
            <h2 className="text-3xl md:text-4xl font-bold">Prêt à Commencer ?</h2>
            <p className="text-lg opacity-90">
              Parcourez nos produits ou contactez-nous directement pour trouver exactement ce dont vous avez besoin
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center pt-4">
              <Link to="/products">
                <Button size="lg" variant="secondary" className="w-full sm:w-auto">
                  Voir les Produits
                </Button>
              </Link>
              <a
                href={`https://wa.me/${whatsappNumber}?text=${whatsappMessage}`}
                target="_blank"
                rel="noopener noreferrer"
              >
                <Button size="lg" variant="outline" className="w-full sm:w-auto bg-transparent text-primary-foreground border-primary-foreground hover:bg-primary-foreground hover:text-primary">
                  <MessageCircle className="mr-2 h-4 w-4" />
                  Écrivez-nous
                </Button>
              </a>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Services;
