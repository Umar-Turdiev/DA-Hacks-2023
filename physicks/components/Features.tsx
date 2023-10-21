import Image from 'next/image';

interface FeatureProps {
  title: string;
  description: string;
  videoSrc: string;
}

function Feature({ title, description, videoSrc }: FeatureProps) {
  return (
    <div className="flex flex-row justify-center mx-8 mb-40 items-center">
      <div className="font-soraR text-2xl w-[40%] mr-32">
        <h4 className="font-sora text-5xl mb-4 text-cyan-500">{title}</h4>
        {description}
      </div>
      <video className="w-[45%] rounded-md" autoPlay muted loop>
        <source src={videoSrc} type="video/mp4" />
        Your browser does not support the video tag.
      </video>
    </div>
  );
}
export default function Features(){
return(
  <div className ="relative w-full flex flex-col items-center">
    <div className="flex flex-col bg-gray-500 bg-opacity-30 w-[95%] rounded-3xl items-center py-16 z-20">
      <Feature
        title="Simulate gravitation"
        description="Allows you to pick different shapes and observe their falling speed and collisions according to their mass"
        videoSrc="/gravity.mp4"
      />
      <Feature
        title="Showcase Newtonian interactions"
        description="Illustrates how objects with different forces applied will interact with each other"
        videoSrc="/arrow.mp4"
      />

      <Feature
        title="Customize Properties"
        description="Explore various options to customize the physical properties of the object"
        videoSrc="/Custom.mp4"
      />
      <Feature
        title="Flexible Sandbox"
        description="Sky's the limit for creativity! Play around with various mechanics"
        videoSrc="/Create.mp4"
      />
    </div>
    <div className="absolute top-96 mt-[600px] left-0">
      <Image
        alt="header text"
        src="/pendal.png"
        width={300}
        height={300}
      />
    </div>
    <div className="absolute bottom-0 right-0 mr-[-100px] mb-[-200px]">
      <Image
        alt="header text"
        src="/planet.jpg"
        width={600}
        height={600}
      />
    </div>
  </div>
);
}