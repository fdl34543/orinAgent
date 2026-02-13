import { useEffect, useRef } from "react";
import { CanvasWrapper, StyledCanvas } from "./map.style";
import { useRouter } from "next/router";

export default function MapCanvas() {
  const canvasRef = useRef(null);
  const router = useRouter();

  const MAP_WIDTH = 2000;
  const MAP_HEIGHT = 1121;

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    const wrapper = canvas.parentElement;

    let viewWidth = wrapper.clientWidth;
    let viewHeight = wrapper.clientHeight;

    canvas.width = viewWidth;
    canvas.height = viewHeight;

    const mapImage = new Image();
    mapImage.src = "/img/map/map1.jpg";

    const cloudImage1 = new Image();
    cloudImage1.src = "/img/map/cloud1.png";

    const cloudImage2 = new Image();
    cloudImage2.src = "/img/map/cloud2.png";

    const hallImage = new Image();
    hallImage.src = "/img/map/hall.png";
    const hospitalImage = new Image();
    hospitalImage.src = "/img/map/hospital.png";
    const cafeImage = new Image();
    cafeImage.src = "/img/map/cafe.png";
    const officeImage = new Image();
    officeImage.src = "/img/map/office.png";
    const policeImage = new Image();
    policeImage.src = "/img/map/police.png";
    const storeImage = new Image();
    storeImage.src = "/img/map/store.png";

    let scale = 1;
    let targetScale = 1;
    let minScale = 1;
    let maxScale = 3;

    let offsetX = 0;
    let offsetY = 0;
    let targetOffsetX = 0;
    let targetOffsetY = 0;

    let isDragging = false;
    let startX = 0;
    let startY = 0;

    const cloudYOffset = -100;

    const clouds = [
      { x: 0, y: 100 + cloudYOffset, speed: 0.3, image: cloudImage1 },
      { x: 1200, y: 150 + cloudYOffset, speed: 0.3, image: cloudImage1 },

      { x: 1800, y: 450 + cloudYOffset, speed: -0.2, image: cloudImage2 },
      { x: 900, y: 500 + cloudYOffset, speed: -0.2, image: cloudImage2 },

      { x: 400, y: 900 + cloudYOffset, speed: 0.15, image: cloudImage1 },
      { x: 1400, y: 950 + cloudYOffset, speed: 0.15, image: cloudImage1 },
    ];

    let hoveredBuilding = null;

    const centerX = MAP_WIDTH / 2;
    const centerY = MAP_HEIGHT / 2;

    const buildings = [
      {
        id: "hall",
        label: "City Hall",
        x: centerX - 150,
        y: centerY - 400,
        width: 300,
        height: 300,
        image: hallImage,
        glow: 0,
      },
      {
        id: "hospital",
        label: "Hospital",
        x: centerX - 650,
        y: centerY - 50,
        width: 220,
        height: 220,
        image: hospitalImage,
        glow: 0,
      },
      {
        id: "cafe",
        label: "Cafe",
        x: centerX + 250,
        y: centerY - 100,
        width: 200,
        height: 200,
        image: cafeImage,
        glow: 0,
      },
      {
        id: "office",
        label: "Office",
        x: centerX - 200,
        y: centerY + 0,
        width: 240,
        height: 240,
        image: officeImage,
        glow: 0,
      },
      {
        id: "police",
        label: "Police Office",
        x: centerX + 350,
        y: centerY + 120,
        width: 220,
        height: 220,
        image: policeImage,
        glow: 0,
      },
      {
        id: "store",
        label: "Store",
        x: centerX - 450,
        y: centerY - 350,
        width: 220,
        height: 220,
        image: storeImage,
        glow: 0,
      },
    ];

    function calculateMinScale() {
      const scaleX = viewWidth / MAP_WIDTH;
      const scaleY = viewHeight / MAP_HEIGHT;
      minScale = Math.max(scaleX, scaleY);
      scale = minScale;
      targetScale = minScale;
    }

    function centerDefault() {
      targetScale = minScale;

      const scaledWidth = MAP_WIDTH * minScale;
      const scaledHeight = MAP_HEIGHT * minScale;

      targetOffsetX = (viewWidth - scaledWidth) / 2;
      targetOffsetY = (viewHeight - scaledHeight) / 2;
    }

    function clampPosition() {
      const scaledWidth = MAP_WIDTH * targetScale;
      const scaledHeight = MAP_HEIGHT * targetScale;

      const minX = viewWidth - scaledWidth;
      const minY = viewHeight - scaledHeight;

      targetOffsetX = Math.min(0, Math.max(minX, targetOffsetX));
      targetOffsetY = Math.min(0, Math.max(minY, targetOffsetY));
    }

    function updateClouds() {
      clouds.forEach((cloud) => {
        cloud.x += cloud.speed;

        if (cloud.speed > 0 && cloud.x > MAP_WIDTH + 400) {
          cloud.x = -500;
        }

        if (cloud.speed < 0 && cloud.x < -500) {
          cloud.x = MAP_WIDTH + 400;
        }
      });
    }

    function screenToWorld(x, y) {
      return {
        worldX: (x - offsetX) / scale,
        worldY: (y - offsetY) / scale,
      };
    }

    function animateCamera() {
      const ease = 0.08;

      scale += (targetScale - scale) * ease;
      offsetX += (targetOffsetX - offsetX) * ease;
      offsetY += (targetOffsetY - offsetY) * ease;
    }

    function draw() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      ctx.save();
      ctx.translate(offsetX, offsetY);
      ctx.scale(scale, scale);

      ctx.drawImage(mapImage, 0, 0, MAP_WIDTH, MAP_HEIGHT);

      clouds.forEach((cloud) => {
        ctx.drawImage(cloud.image, cloud.x, cloud.y, 700, 350);
      });

      buildings.forEach((building) => {
        if (building.glow > 0) {
          ctx.shadowColor = "rgba(255,255,150,0.8)";
          ctx.shadowBlur = 30 * building.glow;
        } else {
          ctx.shadowBlur = 0;
        }

        ctx.shadowOffsetY = 20;
        ctx.shadowColor = "rgba(0,0,0,0.4)";

        ctx.drawImage(
          building.image,
          building.x,
          building.y,
          building.width,
          building.height
        );

        if (hoveredBuilding === building) {
          ctx.save();
          ctx.font = "22px Arial";
          ctx.fillStyle = "white";
          ctx.textAlign = "center";
          ctx.fillText(
            building.label,
            building.x + building.width / 2,
            building.y - 25
          );
          ctx.restore();
        }
      });

      ctx.restore();
    }

    function startDrag(x, y) {
      if (scale === minScale && window.innerWidth > 768) return;

      isDragging = true;
      startX = x - targetOffsetX;
      startY = y - targetOffsetY;
    }

    function drag(x, y) {
      if (!isDragging) return;

      targetOffsetX = x - startX;
      targetOffsetY = y - startY;

      clampPosition();
    }

    function endDrag() {
      isDragging = false;
    }

    function focusBuilding(building) {
      const targetZoom = 2;

      const worldCenterX = building.x + building.width / 2;
      const worldCenterY = building.y + building.height / 2;

      targetScale = targetZoom;

      targetOffsetX = viewWidth / 2 - worldCenterX * targetZoom;
      targetOffsetY = viewHeight / 2 - worldCenterY * targetZoom;

      clampPosition();
    }

    function zoom(delta, x, y) {
      const zoomSpeed = 0.1;

      const previousScale = targetScale;

      if (delta > 0) targetScale -= zoomSpeed;
      else targetScale += zoomSpeed;

      targetScale = Math.max(minScale, Math.min(maxScale, targetScale));

      const worldX = (x - offsetX) / scale;
      const worldY = (y - offsetY) / scale;

      targetOffsetX = x - worldX * targetScale;
      targetOffsetY = y - worldY * targetScale;

      clampPosition();
    }

    function handleBuildingAction(id) {
      const locationMap = {
        hall: "Hall",
        hospital: "Hospital",
        cafe: "Cafe",
        office: "Office",
        police: "Police",
        store: "Store",
      };

      const locationName = locationMap[id];
      if (!locationName) return;

      router.push(
        {
          pathname: "/world",
          query: { location: locationName },
        },
        undefined,
        { shallow: true }
      );
    }

    function loop() {
      updateClouds();
      buildings.forEach((b) => {
        if (hoveredBuilding === b) {
          b.glow += (1 - b.glow) * 0.1;
        } else {
          b.glow += (0 - b.glow) * 0.1;
        }
      });

      animateCamera();
      draw();
      requestAnimationFrame(loop);
    }

    mapImage.onload = () => {
      calculateMinScale();
      centerDefault();
      loop();
    };

    canvas.addEventListener("mousemove", (e) => {
      const rect = canvas.getBoundingClientRect();
      const { worldX, worldY } = screenToWorld(
        e.clientX - rect.left,
        e.clientY - rect.top
      );

      hoveredBuilding = null;

      buildings.forEach((building) => {
        if (
          worldX >= building.x &&
          worldX <= building.x + building.width &&
          worldY >= building.y &&
          worldY <= building.y + building.height
        ) {
          hoveredBuilding = building;
        }
      });

      canvas.style.cursor =
        hoveredBuilding ? "pointer" : "grab";
    });

    canvas.addEventListener("click", (e) => {
      if (!hoveredBuilding) {
        centerDefault();
        router.push("/world", undefined, { shallow: true });
        return;
      }

      focusBuilding(hoveredBuilding);

      handleBuildingAction(hoveredBuilding.id);
    });

    canvas.addEventListener("mousedown", (e) =>
      startDrag(e.clientX, e.clientY)
    );

    canvas.addEventListener("mousemove", (e) =>
      drag(e.clientX, e.clientY)
    );

    canvas.addEventListener("mouseup", endDrag);
    canvas.addEventListener("mouseleave", endDrag);

    canvas.addEventListener("wheel", (e) => {
      e.preventDefault();
      zoom(e.deltaY, e.clientX, e.clientY);
    });
    
    canvas.addEventListener("touchstart", (e) => {
      const touch = e.touches[0];
      startDrag(touch.clientX, touch.clientY);
    });

    canvas.addEventListener("touchmove", (e) => {
      const touch = e.touches[0];
      drag(touch.clientX, touch.clientY);
    });

    canvas.addEventListener("touchend", endDrag);

  }, []);

  return (
    <CanvasWrapper>
      <StyledCanvas ref={canvasRef} />
    </CanvasWrapper>
  );
}
