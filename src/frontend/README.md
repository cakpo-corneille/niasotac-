# NIASOTAC Frontend - Interface Client

## Description

Interface utilisateur moderne et réactive pour la vitrine e-commerce NIASOTAC. Construite avec React 18, TypeScript et Vite, utilisant shadcn/ui pour les composants UI et Tailwind CSS pour le styling.

## Technologies Utilisées

- **React 18.3** - Bibliothèque UI JavaScript
- **TypeScript 5.8** - JavaScript typé
- **Vite 5.4** - Build tool et dev server ultra-rapide
- **Tailwind CSS 3.4** - Framework CSS utility-first
- **shadcn/ui** - Collection de composants UI réutilisables
- **React Router 6** - Routage côté client
- **TanStack Query 5** - Gestion de l'état serveur et cache
- **Lucide React** - Bibliothèque d'icônes

## Installation Locale

### Prérequis

- Node.js 20.x ou supérieur
- npm 10.x ou supérieur (inclus avec Node.js)

### Étapes d'Installation

1. **Naviguer vers le dossier frontend**
   ```bash
   cd frontend
   ```

2. **Installer les dépendances**
   ```bash
   npm install
   ```

3. **Démarrer le serveur de développement**
   ```bash
   npm run dev
   ```

   L'application démarre sur `http://localhost:5000/`

4. **Ouvrir dans le navigateur**
   
   Accéder à `http://localhost:5000` pour voir l'application.

## Scripts Disponibles

### Développement

```bash
# Démarrer le serveur de développement avec hot reload
npm run dev
```

### Production

```bash
# Construire l'application pour la production
npm run build

# Prévisualiser le build de production
npm run preview

# Construire en mode développement
npm run build:dev
```

### Qualité du Code

```bash
# Linter le code (vérifier les erreurs)
npm run lint
```

## Structure du Projet

```
frontend/
├── src/
│   ├── components/          # Composants React
│   │   ├── ui/             # Composants UI shadcn
│   │   ├── Navbar.tsx      # Barre de navigation
│   │   ├── Footer.tsx      # Pied de page
│   │   ├── HeroSection.tsx # Section héro page d'accueil
│   │   ├── ProductCard.tsx # Carte produit
│   │   ├── CategoryCard.tsx # Carte catégorie
│   │   ├── ContactForm.tsx  # Formulaire de contact
│   │   └── WhatsAppButton.tsx # Bouton WhatsApp flottant
│   │
│   ├── pages/              # Pages de l'application
│   │   ├── Home.tsx        # Page d'accueil
│   │   ├── Products.tsx    # Page catalogue produits
│   │   ├── ProductDetail.tsx # Détails d'un produit
│   │   ├── Services.tsx    # Page services
│   │   ├── Contact.tsx     # Page contact
│   │   └── NotFound.tsx    # Page 404
│   │
│   ├── hooks/              # Custom React hooks
│   │   ├── useCategories.ts # Hook pour les catégories
│   │   ├── useProducts.ts   # Hook pour les produits
│   │   ├── useSiteSettings.ts # Hook pour les paramètres
│   │   ├── use-mobile.tsx   # Hook détection mobile
│   │   └── use-toast.ts     # Hook notifications toast
│   │
│   ├── lib/                # Utilitaires et configuration
│   │   ├── api.ts          # Configuration API et fonctions fetch
│   │   └── utils.ts        # Fonctions utilitaires
│   │
│   ├── data/               # Données mock (non utilisées actuellement)
│   │   └── mockData.ts
│   │
│   ├── assets/             # Ressources statiques
│   │   └── hero-image.jpg
│   │
│   ├── App.tsx             # Composant racine avec routes
│   ├── main.tsx            # Point d'entrée de l'application
│   └── index.css           # Styles globaux Tailwind
│
├── public/                 # Fichiers statiques publics
│   ├── favicon.ico
│   ├── placeholder.svg
│   └── robots.txt
│
├── index.html             # Template HTML
├── vite.config.ts         # Configuration Vite
├── tailwind.config.ts     # Configuration Tailwind
├── tsconfig.json          # Configuration TypeScript
├── postcss.config.js      # Configuration PostCSS
├── eslint.config.js       # Configuration ESLint
└── package.json           # Dépendances et scripts
```

## Pages de l'Application

### 1. Page d'Accueil (/)
- Section héro avec image et call-to-action
- Produits vedettes affichés
- Catégories principales
- Statistiques de l'entreprise
- Bouton WhatsApp flottant

### 2. Catalogue Produits (/produits)
- Liste de tous les produits
- Filtrage par catégorie/sous-catégorie
- Filtrage par disponibilité
- Recherche par nom/marque
- Pagination automatique
- Cartes produits avec prix et image

### 3. Détails Produit (/produits/:slug)
- Image du produit en grand
- Description complète
- Prix en FCFA
- Marque et catégorie
- Indication de disponibilité
- Bouton WhatsApp pour commander

### 4. Services (/services)
- Présentation des services offerts
- Vente de matériel informatique
- Installation et configuration
- Support technique
- Maintenance

### 5. Contact (/contact)
- Formulaire de contact
- Informations de contact
- Adresse et téléphone
- Email
- Lien WhatsApp direct

## Configuration de l'API

### Proxy Vite pour le Développement

Le fichier `vite.config.ts` est configuré pour proxifier les requêtes API vers le backend Django :

```typescript
server: {
  host: "0.0.0.0",
  port: 5000,
  allowedHosts: true,
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
      secure: false,
    },
  },
}
```

Cela permet d'appeler l'API via `/api/products/` qui est automatiquement redirigé vers `http://localhost:8000/api/products/`.

### Configuration API (src/lib/api.ts)

```typescript
export const API_BASE_URL = '/api';

export const api = {
  get: async (endpoint: string) => {
    const response = await fetch(`${API_BASE_URL}${endpoint}`);
    if (!response.ok) throw new Error('API request failed');
    return response.json();
  },
  // ...
};
```

## Custom Hooks

### useCategories
Récupère et gère les catégories depuis l'API.

```typescript
import { useCategories } from '@/hooks/useCategories';

const { data: categories, isLoading, error } = useCategories();
```

### useProducts
Récupère et gère les produits avec filtres optionnels.

```typescript
import { useProducts } from '@/hooks/useProducts';

const { data: products, isLoading } = useProducts({ 
  featured: true,
  category: categoryId 
});
```

### useSiteSettings
Récupère les paramètres du site (WhatsApp, contact, etc.).

```typescript
import { useSiteSettings } from '@/hooks/useSiteSettings';

const { data: settings } = useSiteSettings();
```

## Composants shadcn/ui Utilisés

Le projet utilise plusieurs composants de shadcn/ui :
- `Button` - Boutons stylisés
- `Card` - Cartes pour produits et catégories
- `Input` - Champs de saisie
- `Badge` - Badges de statut
- `Separator` - Séparateurs visuels
- `Sheet` - Menus latéraux
- `Toast` - Notifications
- `Skeleton` - Placeholders de chargement

Pour ajouter un nouveau composant shadcn/ui :
```bash
npx shadcn@latest add [nom-du-composant]
```

## Styling avec Tailwind CSS

Le projet utilise Tailwind CSS pour tous les styles. Classes utilitaires principales utilisées :

```tsx
// Exemple de card produit
<div className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow">
  <img className="w-full h-48 object-cover rounded-t-lg" />
  <div className="p-4">
    <h3 className="text-lg font-semibold text-gray-800">Nom du produit</h3>
    <p className="text-blue-600 font-bold">Prix FCFA</p>
  </div>
</div>
```

### Configuration Tailwind

Les couleurs et thèmes personnalisés sont définis dans `tailwind.config.ts`.

## Routage

React Router 6 est utilisé pour le routage :

```typescript
<Routes>
  <Route path="/" element={<Home />} />
  <Route path="/produits" element={<Products />} />
  <Route path="/produits/:slug" element={<ProductDetail />} />
  <Route path="/services" element={<Services />} />
  <Route path="/contact" element={<Contact />} />
  <Route path="*" element={<NotFound />} />
</Routes>
```

## Intégration WhatsApp

### Bouton Flottant
Un bouton WhatsApp flottant est présent sur toutes les pages :

```typescript
<WhatsAppButton />
```

### Messages Pré-remplis pour Produits
Chaque produit a un lien WhatsApp avec message pré-rempli généré côté backend.

## Optimisation et Performance

### Code Splitting
Vite gère automatiquement le code splitting pour optimiser les temps de chargement.

### Lazy Loading Images
Les images sont chargées avec l'attribut `loading="lazy"` pour améliorer les performances.

### TanStack Query Cache
Les requêtes API sont mises en cache automatiquement par TanStack Query, réduisant les appels réseau.

### Production Build
```bash
npm run build
```

Crée un build optimisé dans le dossier `dist/` avec :
- Minification du code
- Tree shaking pour éliminer le code inutilisé
- Optimisation des images
- Hachage des fichiers pour le cache

## Variables d'Environnement

Créer un fichier `.env` (optionnel) pour surcharger la configuration :

```env
VITE_API_URL=http://localhost:8000
```

Utilisation dans le code :
```typescript
const apiUrl = import.meta.env.VITE_API_URL || '/api';
```

## Déploiement

### Build de Production

```bash
npm run build
```

Les fichiers de production sont générés dans `dist/` et peuvent être :
- Servis par n'importe quel serveur web static (nginx, Apache)
- Déployés sur Netlify, Vercel, ou autre plateforme
- Intégrés avec Django (via WhiteNoise) comme dans ce projet

### Vérifier le Build Localement

```bash
npm run preview
```

Cela démarre un serveur local servant les fichiers du dossier `dist/`.

## Dépannage

### Problème : "Cannot find module '@/...' "
```bash
# Vérifier les alias TypeScript dans tsconfig.json
# Réinstaller les dépendances
rm -rf node_modules package-lock.json
npm install
```

### Problème : Erreurs de compilation TypeScript
```bash
# Vérifier les types
npm run build

# Corriger les erreurs TypeScript signalées
```

### Problème : API non accessible
1. Vérifier que le backend Django tourne sur le port 8000
2. Vérifier la configuration du proxy dans `vite.config.ts`
3. Inspecter la console navigateur pour voir les erreurs réseau

### Problème : Hot reload ne fonctionne pas
```bash
# Redémarrer le serveur de développement
# Ctrl+C pour arrêter
npm run dev
```

### Problème : Styles Tailwind non appliqués
```bash
# Vérifier que PostCSS et Tailwind sont installés
npm install -D tailwindcss postcss autoprefixer

# Vérifier tailwind.config.ts - content doit inclure src/**/*.tsx
```

## Bonnes Pratiques

1. **Composants Réutilisables** : Créer des composants modulaires et réutilisables
2. **TypeScript** : Typer toutes les props et données API
3. **Hooks Personnalisés** : Encapsuler la logique réutilisable dans des hooks
4. **Gestion d'État** : Utiliser TanStack Query pour les données serveur
5. **Accessibilité** : Utiliser les attributs aria-* et semantic HTML
6. **Responsive Design** : Tester sur mobile, tablette et desktop
7. **Performance** : Lazy load, code splitting, optimisation images

## Support

Pour toute question ou problème :
- Documentation React : https://react.dev/
- Documentation Vite : https://vite.dev/
- Documentation Tailwind : https://tailwindcss.com/
- Documentation shadcn/ui : https://ui.shadcn.com/

## Licence

Ce projet est privé et destiné à un usage interne.
