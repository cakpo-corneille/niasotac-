import { MessageCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';

export const WhatsAppButton = () => {
  const whatsappNumber = '+22900000000';
  const whatsappMessage = encodeURIComponent('Hello! I am interested in your tech products.');

  return (
    <a
      href={`https://wa.me/${whatsappNumber}?text=${whatsappMessage}`}
      target="_blank"
      rel="noopener noreferrer"
      className="fixed bottom-6 right-6 z-50 animate-fade-in"
    >
      <Button
        size="lg"
        className="rounded-full shadow-lg hover:scale-110 transition-transform group"
      >
        <MessageCircle className="h-5 w-5 group-hover:animate-pulse" />
        <span className="ml-2">WhatsApp</span>
      </Button>
    </a>
  );
};
