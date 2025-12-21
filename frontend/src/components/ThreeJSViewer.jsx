import React, { useEffect, useRef } from "react";
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";

const ThreeJSViewer = () => {
  const containerRef = useRef(null);

  useEffect(() => {
    let scene, camera, renderer, controls;
    let worksheet1, worksheet2;
    const clock = new THREE.Clock();

    const container = containerRef.current;
    if (!container) return;

    // === Scene setup ===
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0xffffff);

    camera = new THREE.PerspectiveCamera(
      50,
      container.clientWidth / container.clientHeight,
      0.1,
      1000
    );
    camera.position.set(0, 0, 5);

    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(container.clientWidth, container.clientHeight);

    // NEW Three.js API:
    // Replace outputEncoding with outputColorSpace
    renderer.outputColorSpace = THREE.SRGBColorSpace;

    container.appendChild(renderer.domElement);

    controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.minDistance = 3;
    controls.maxDistance = 10;
    controls.enableZoom = false;

    // === Lighting ===
    const ambientLight = new THREE.AmbientLight(0xffffff, 1.2);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
    directionalLight.position.set(5, 5, 5);
    scene.add(directionalLight);

    // === Load Textures ===
    const loader = new THREE.TextureLoader();
    const texture1 = loader.load("/images/basic_addition.png");
    const texture2 = loader.load("/images/quadratic.png");

    // Updated texture colorspace and filters
    [texture1, texture2].forEach((texture) => {
      texture.colorSpace = THREE.SRGBColorSpace;
      texture.minFilter = THREE.NearestFilter;
      texture.magFilter = THREE.NearestFilter;
    });

    // === Materials ===
    const material1 = new THREE.MeshBasicMaterial({
      map: texture1,
      side: THREE.DoubleSide,
      opacity: 1.0,
      transparent: false,
    });

    const material2 = new THREE.MeshBasicMaterial({
      map: texture2,
      side: THREE.DoubleSide,
      opacity: 1.0,
      transparent: false,
    });

    // === Geometry and Meshes ===
    const geometry = new THREE.PlaneGeometry(3, 4);
    worksheet1 = new THREE.Mesh(geometry, material1);
    worksheet2 = new THREE.Mesh(geometry, material2);

    worksheet1.position.set(-2, 0, 0);
    worksheet2.position.set(2, 0, 0);

    worksheet1.rotation.set(0, Math.PI / 6, 0);
    worksheet2.rotation.set(0, -Math.PI / 6, 0);

    scene.add(worksheet1);
    scene.add(worksheet2);

    // === Animation ===
    const animate = () => {
      requestAnimationFrame(animate);
      const time = clock.getElapsedTime();
      worksheet1.position.y = Math.sin(time) * 0.3;
      worksheet2.position.y = Math.sin(time + Math.PI) * 0.3;
      controls.update();
      renderer.render(scene, camera);
    };
    animate();

    // === Resize Handling ===
    const handleResize = () => {
      camera.aspect = container.clientWidth / container.clientHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(container.clientWidth, container.clientHeight);
    };

    window.addEventListener("resize", handleResize);
    return () => {
      window.removeEventListener("resize", handleResize);
      container.removeChild(renderer.domElement);
    };
  }, []);

  return <div id="threejs-container" ref={containerRef}></div>;
};

export default ThreeJSViewer;
