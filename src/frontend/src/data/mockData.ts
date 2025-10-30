export interface Product {
  id: string;
  name: string;
  description: string;
  price: number;
  image: string;
  category: string;
  subcategory: string;
  featured?: boolean;
  specifications?: Record<string, string>;
}

export interface Category {
  id: string;
  name: string;
  description: string;
  subcategories: Subcategory[];
}

export interface Subcategory {
  id: string;
  name: string;
  categoryId: string;
}

export const categories: Category[] = [
  {
    id: 'computers',
    name: 'Computers',
    description: 'Desktop computers, laptops, and all-in-one systems',
    subcategories: [
      { id: 'laptops', name: 'Laptops', categoryId: 'computers' },
      { id: 'desktops', name: 'Desktop PCs', categoryId: 'computers' },
      { id: 'tablets', name: 'Tablets', categoryId: 'computers' },
    ],
  },
  {
    id: 'components',
    name: 'Components',
    description: 'Computer parts and hardware components',
    subcategories: [
      { id: 'processors', name: 'Processors', categoryId: 'components' },
      { id: 'memory', name: 'Memory & Storage', categoryId: 'components' },
      { id: 'graphics', name: 'Graphics Cards', categoryId: 'components' },
    ],
  },
  {
    id: 'printers',
    name: 'Printers',
    description: 'Printers and printing solutions',
    subcategories: [
      { id: 'inkjet', name: 'Inkjet Printers', categoryId: 'printers' },
      { id: 'laser', name: 'Laser Printers', categoryId: 'printers' },
      { id: 'multifunction', name: 'Multifunction Printers', categoryId: 'printers' },
    ],
  },
  {
    id: 'accessories',
    name: 'Accessories',
    description: 'Peripherals and computer accessories',
    subcategories: [
      { id: 'keyboards', name: 'Keyboards & Mice', categoryId: 'accessories' },
      { id: 'monitors', name: 'Monitors', categoryId: 'accessories' },
      { id: 'audio', name: 'Audio Devices', categoryId: 'accessories' },
    ],
  },
];

export const products: Product[] = [
  // Laptops
  {
    id: '1',
    name: 'HP Pavilion 15',
    description: 'Powerful laptop with Intel Core i5, 8GB RAM, 512GB SSD',
    price: 450000,
    image: 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=500',
    category: 'computers',
    subcategory: 'laptops',
    featured: true,
    specifications: {
      Processor: 'Intel Core i5',
      RAM: '8GB DDR4',
      Storage: '512GB SSD',
      Display: '15.6" Full HD',
    },
  },
  {
    id: '2',
    name: 'Dell Inspiron 14',
    description: 'Compact and efficient laptop for everyday computing',
    price: 380000,
    image: 'https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=500',
    category: 'computers',
    subcategory: 'laptops',
    specifications: {
      Processor: 'Intel Core i3',
      RAM: '8GB DDR4',
      Storage: '256GB SSD',
      Display: '14" HD',
    },
  },
  {
    id: '3',
    name: 'Lenovo ThinkPad E15',
    description: 'Business-grade laptop with excellent build quality',
    price: 520000,
    image: 'https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=500',
    category: 'computers',
    subcategory: 'laptops',
    featured: true,
    specifications: {
      Processor: 'Intel Core i5',
      RAM: '16GB DDR4',
      Storage: '512GB SSD',
      Display: '15.6" Full HD',
    },
  },
  
  // Desktop PCs
  {
    id: '4',
    name: 'HP Elite Desktop',
    description: 'Powerful desktop PC for office and home use',
    price: 320000,
    image: 'https://images.unsplash.com/photo-1587202372634-32705e3bf49c?w=500',
    category: 'computers',
    subcategory: 'desktops',
    specifications: {
      Processor: 'Intel Core i5',
      RAM: '8GB DDR4',
      Storage: '1TB HDD',
    },
  },
  {
    id: '5',
    name: 'Dell OptiPlex Tower',
    description: 'Reliable desktop computer for professional use',
    price: 280000,
    image: 'https://images.unsplash.com/photo-1593640408182-31c70c8268f5?w=500',
    category: 'computers',
    subcategory: 'desktops',
  },
  
  // Processors
  {
    id: '6',
    name: 'Intel Core i7-12700K',
    description: 'High-performance processor for gaming and productivity',
    price: 185000,
    image: 'https://images.unsplash.com/photo-1555680202-c86f0e12f086?w=500',
    category: 'components',
    subcategory: 'processors',
    featured: true,
  },
  {
    id: '7',
    name: 'AMD Ryzen 5 5600X',
    description: 'Excellent mid-range processor with great value',
    price: 125000,
    image: 'https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?w=500',
    category: 'components',
    subcategory: 'processors',
  },
  
  // Memory & Storage
  {
    id: '8',
    name: 'Kingston 16GB DDR4 RAM',
    description: 'High-speed memory for improved performance',
    price: 35000,
    image: 'https://images.unsplash.com/photo-1562976540-1502c2145186?w=500',
    category: 'components',
    subcategory: 'memory',
  },
  {
    id: '9',
    name: 'Samsung 1TB SSD',
    description: 'Fast and reliable solid-state drive',
    price: 65000,
    image: 'https://images.unsplash.com/photo-1531492746076-161ca9bcad58?w=500',
    category: 'components',
    subcategory: 'memory',
  },
  {
    id: '10',
    name: 'Seagate 2TB HDD',
    description: 'Large capacity hard drive for data storage',
    price: 45000,
    image: 'https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?w=500',
    category: 'components',
    subcategory: 'memory',
  },
  
  // Graphics Cards
  {
    id: '11',
    name: 'NVIDIA RTX 3060',
    description: 'Powerful graphics card for gaming and content creation',
    price: 295000,
    image: 'https://images.unsplash.com/photo-1591488320449-011701bb6704?w=500',
    category: 'components',
    subcategory: 'graphics',
    featured: true,
  },
  
  // Printers
  {
    id: '12',
    name: 'HP DeskJet 2720',
    description: 'All-in-one wireless inkjet printer',
    price: 85000,
    image: 'https://images.unsplash.com/photo-1612815154858-60aa4c59eaa6?w=500',
    category: 'printers',
    subcategory: 'inkjet',
  },
  {
    id: '13',
    name: 'Canon PIXMA TS3350',
    description: 'Compact wireless printer for home use',
    price: 72000,
    image: 'https://images.unsplash.com/photo-1606800052052-be6f7b0a2e2a?w=500',
    category: 'printers',
    subcategory: 'inkjet',
  },
  {
    id: '14',
    name: 'Brother HL-L2350DW',
    description: 'Fast monochrome laser printer',
    price: 125000,
    image: 'https://images.unsplash.com/photo-1596526131083-e8c633c948d2?w=500',
    category: 'printers',
    subcategory: 'laser',
  },
  {
    id: '15',
    name: 'Epson EcoTank L3250',
    description: 'Economical multifunction printer with tank system',
    price: 165000,
    image: 'https://images.unsplash.com/photo-1590872256693-1ed0c40c8548?w=500',
    category: 'printers',
    subcategory: 'multifunction',
  },
  
  // Accessories
  {
    id: '16',
    name: 'Logitech MK270 Combo',
    description: 'Wireless keyboard and mouse combo',
    price: 25000,
    image: 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=500',
    category: 'accessories',
    subcategory: 'keyboards',
  },
  {
    id: '17',
    name: 'Razer DeathAdder V2',
    description: 'Ergonomic gaming mouse with high precision',
    price: 38000,
    image: 'https://images.unsplash.com/photo-1527814050087-3793815479db?w=500',
    category: 'accessories',
    subcategory: 'keyboards',
  },
  {
    id: '18',
    name: 'LG 24" Full HD Monitor',
    description: 'IPS display with excellent color accuracy',
    price: 95000,
    image: 'https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=500',
    category: 'accessories',
    subcategory: 'monitors',
    featured: true,
  },
  {
    id: '19',
    name: 'Dell 27" 4K Monitor',
    description: 'Ultra HD display for professionals',
    price: 185000,
    image: 'https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=500',
    category: 'accessories',
    subcategory: 'monitors',
  },
  {
    id: '20',
    name: 'JBL Quantum 100',
    description: 'Gaming headset with clear audio',
    price: 32000,
    image: 'https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=500',
    category: 'accessories',
    subcategory: 'audio',
  },
];
