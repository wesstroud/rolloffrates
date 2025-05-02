import React from 'react';

interface DumpsterCardProps {
  size: number;
  title: string;
  description: string;
  price: string;
  imagePath: string;
}

const DumpsterCard: React.FC<DumpsterCardProps> = ({ size, title, description, price, imagePath }) => {
  return (
    <div className="border rounded-lg overflow-hidden shadow-md hover:shadow-lg transition-shadow">
      <div className="h-48 overflow-hidden">
        <img 
          src={imagePath} 
          alt={`${size} Yard Dumpster`} 
          className="w-full h-full object-cover"
        />
      </div>
      <div className="p-6">
        <h3 className="text-xl font-bold mb-2">{title}</h3>
        <p className="text-gray-600 mb-4">{description}</p>
        <div className="flex justify-between items-center">
          <div>
            <span className="text-gray-500">Starting at</span>
            <p className="text-2xl font-bold text-green-600">{price}</p>
          </div>
          <a 
            href="#" 
            className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition"
          >
            Get a Quote
          </a>
        </div>
      </div>
    </div>
  );
};

export const DumpsterCards: React.FC = () => {
  const dumpsterSizes = [
    {
      size: 10,
      title: "10 Yard Dumpster",
      description: "Perfect for small remodeling projects, garage cleanouts, or small amounts of construction debris.",
      price: "$299",
      imagePath: "/images/pexels-reneterp-3990359.jpg" // Using the provided image for 10-yard dumpster
    },
    {
      size: 20,
      title: "20 Yard Dumpster",
      description: "Ideal for medium-sized projects, home renovations, or larger cleanouts.",
      price: "$399",
      imagePath: "https://placehold.co/600x400/e2e8f0/1e293b?text=20+Yard+Dumpster"
    },
    {
      size: 30,
      title: "30 Yard Dumpster",
      description: "Great for major renovations, new construction, or large-scale cleanouts.",
      price: "$499",
      imagePath: "https://placehold.co/600x400/e2e8f0/1e293b?text=30+Yard+Dumpster"
    },
    {
      size: 40,
      title: "40 Yard Dumpster",
      description: "Best for commercial projects, major construction, or whole-house cleanouts.",
      price: "$599",
      imagePath: "https://placehold.co/600x400/e2e8f0/1e293b?text=40+Yard+Dumpster"
    }
  ];

  return (
    <section className="my-12">
      <h2 className="text-3xl font-bold mb-6 text-center">Popular Dumpster Sizes</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {dumpsterSizes.map((dumpster) => (
          <DumpsterCard
            key={dumpster.size}
            size={dumpster.size}
            title={dumpster.title}
            description={dumpster.description}
            price={dumpster.price}
            imagePath={dumpster.imagePath}
          />
        ))}
      </div>
    </section>
  );
};
