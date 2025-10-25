import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Camera, TrendingUp, MessageSquare, ShoppingCart, CheckCircle2, MessageCircle } from 'lucide-react';
import { Link } from 'react-router-dom';

const Services = () => {
  const whatsappNumber = '+22900000000';
  const whatsappMessage = encodeURIComponent('Hello! I would like to know more about your services.');

  const services = [
    {
      icon: Camera,
      title: 'Product Photography',
      description: 'We visit partner electronics stores across Benin and take high-quality photos of their products, ensuring every detail is captured professionally.',
      benefits: [
        'Professional product images',
        'Multiple angles and views',
        'High-resolution photos',
        'Quick turnaround time',
      ],
    },
    {
      icon: TrendingUp,
      title: 'Online Promotion',
      description: 'We promote products through our website and social media channels, reaching customers who are actively looking for tech products.',
      benefits: [
        'Wide online reach',
        'Targeted marketing',
        'Social media presence',
        'SEO-optimized listings',
      ],
    },
    {
      icon: MessageSquare,
      title: 'Price Negotiation',
      description: 'We work with our partner stores to negotiate the best possible prices for our customers, ensuring you get great value for your money.',
      benefits: [
        'Competitive pricing',
        'Bulk discounts available',
        'Direct store relationships',
        'Transparent pricing',
      ],
    },
    {
      icon: ShoppingCart,
      title: 'Direct Sales',
      description: 'We handle the entire sales process from inquiry to delivery, making it easy and convenient for you to get the tech products you need.',
      benefits: [
        'Simple ordering process',
        'Fast delivery',
        'Secure transactions',
        '24/7 WhatsApp support',
      ],
    },
  ];

  return (
    <div className="flex flex-col min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-b from-primary/5 to-background py-16 md:py-24 border-b">
        <div className="container mx-auto px-4">
          <div className="max-w-3xl mx-auto text-center space-y-6">
            <h1 className="text-4xl md:text-5xl font-bold">Our Services</h1>
            <p className="text-xl text-muted-foreground">
              We bridge the gap between tech stores and customers, making quality products 
              accessible and affordable across Benin
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center pt-4">
              <Link to="/products">
                <Button size="lg">
                  Browse Products
                </Button>
              </Link>
              <a
                href={`https://wa.me/${whatsappNumber}?text=${whatsappMessage}`}
                target="_blank"
                rel="noopener noreferrer"
              >
                <Button size="lg" variant="outline">
                  <MessageCircle className="mr-2 h-4 w-4" />
                  Contact Us
                </Button>
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">How We Work</h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              Our streamlined process ensures you get the best products at the best prices
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 max-w-6xl mx-auto">
            {[
              { step: '1', title: 'Visit Stores', desc: 'We visit partner electronics stores' },
              { step: '2', title: 'Document Products', desc: 'Take photos and gather product details' },
              { step: '3', title: 'List Online', desc: 'Publish products on our website' },
              { step: '4', title: 'Connect & Sell', desc: 'Connect customers with best deals' },
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

      {/* Services Detail */}
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

      {/* Why Choose Us */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto">
            <div className="text-center mb-12">
              <h2 className="text-3xl md:text-4xl font-bold mb-4">Why Choose NIASOTAC?</h2>
              <p className="text-muted-foreground">
                We're more than just a reseller - we're your trusted tech partner
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {[
                {
                  title: 'Extensive Network',
                  desc: 'We partner with 50+ electronics stores across Benin, giving you access to the widest selection of products.',
                },
                {
                  title: 'Competitive Prices',
                  desc: 'Our strong relationships with stores allow us to negotiate better prices for you.',
                },
                {
                  title: 'Quality Assurance',
                  desc: 'Every product is verified before being listed, ensuring you get genuine, quality items.',
                },
                {
                  title: 'Always Available',
                  desc: '24/7 support via WhatsApp means we\'re here whenever you need assistance.',
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

      {/* CTA Section */}
      <section className="py-16 bg-gradient-to-r from-primary to-primary/80 text-primary-foreground">
        <div className="container mx-auto px-4">
          <div className="max-w-3xl mx-auto text-center space-y-6">
            <h2 className="text-3xl md:text-4xl font-bold">Ready to Get Started?</h2>
            <p className="text-lg opacity-90">
              Browse our products or contact us directly to find exactly what you need
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center pt-4">
              <Link to="/products">
                <Button size="lg" variant="secondary" className="w-full sm:w-auto">
                  View Products
                </Button>
              </Link>
              <a
                href={`https://wa.me/${whatsappNumber}?text=${whatsappMessage}`}
                target="_blank"
                rel="noopener noreferrer"
              >
                <Button size="lg" variant="outline" className="w-full sm:w-auto bg-transparent text-primary-foreground border-primary-foreground hover:bg-primary-foreground hover:text-primary">
                  <MessageCircle className="mr-2 h-4 w-4" />
                  WhatsApp Us
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
