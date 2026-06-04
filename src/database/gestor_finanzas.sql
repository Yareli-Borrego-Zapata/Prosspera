-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         10.4.28-MariaDB - mariadb.org binary distribution
-- SO del servidor:              Win64
-- HeidiSQL Versión:             12.17.0.7270
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Volcando estructura de base de datos para gestor_finanzas
CREATE DATABASE IF NOT EXISTS `gestor_finanzas` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `gestor_finanzas`;

-- Volcando estructura para tabla gestor_finanzas.categorias
CREATE TABLE IF NOT EXISTS `categorias` (
  `id_categoria` int(11) NOT NULL AUTO_INCREMENT,
  `nombre_categoria` varchar(50) NOT NULL,
  `tipo` enum('Ingreso','Gasto') NOT NULL,
  PRIMARY KEY (`id_categoria`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla gestor_finanzas.categorias: ~8 rows (aproximadamente)
DELETE FROM `categorias`;
INSERT INTO `categorias` (`id_categoria`, `nombre_categoria`, `tipo`) VALUES
	(1, 'Sueldo', 'Ingreso'),
	(2, 'Ventas', 'Ingreso'),
	(3, 'Comida', 'Gasto'),
	(4, 'Transporte', 'Gasto'),
	(5, 'Escuela', 'Gasto'),
	(6, 'Entretenimiento', 'Gasto'),
	(7, 'Salud', 'Gasto'),
	(8, 'Ahorro', 'Ingreso');

-- Volcando estructura para tabla gestor_finanzas.metas_ahorro
CREATE TABLE IF NOT EXISTS `metas_ahorro` (
  `id_meta` int(11) NOT NULL AUTO_INCREMENT,
  `id_usuario` int(11) NOT NULL,
  `nombre_meta` varchar(100) NOT NULL,
  `monto_objetivo` decimal(10,2) NOT NULL,
  `monto_actual` decimal(10,2) DEFAULT 0.00,
  `fecha_limite` date DEFAULT NULL,
  PRIMARY KEY (`id_meta`),
  KEY `fk_usuario_meta` (`id_usuario`),
  CONSTRAINT `fk_usuario_meta` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla gestor_finanzas.metas_ahorro: ~0 rows (aproximadamente)
DELETE FROM `metas_ahorro`;

-- Volcando estructura para tabla gestor_finanzas.presupuestos
CREATE TABLE IF NOT EXISTS `presupuestos` (
  `id_presupuesto` int(11) NOT NULL AUTO_INCREMENT,
  `id_usuario` int(11) NOT NULL,
  `id_categoria` int(11) NOT NULL,
  `monto_limite` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id_presupuesto`),
  KEY `fk_usuario_presupuesto` (`id_usuario`),
  KEY `fk_categoria_presupuesto` (`id_categoria`),
  CONSTRAINT `fk_categoria_presupuesto` FOREIGN KEY (`id_categoria`) REFERENCES `categorias` (`id_categoria`) ON DELETE CASCADE,
  CONSTRAINT `fk_usuario_presupuesto` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla gestor_finanzas.presupuestos: ~0 rows (aproximadamente)
DELETE FROM `presupuestos`;

-- Volcando estructura para tabla gestor_finanzas.transacciones
CREATE TABLE IF NOT EXISTS `transacciones` (
  `id_transaccion` int(11) NOT NULL AUTO_INCREMENT,
  `id_usuario` int(11) NOT NULL,
  `id_categoria` int(11) NOT NULL,
  `monto` decimal(10,2) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `fecha` date NOT NULL,
  PRIMARY KEY (`id_transaccion`),
  KEY `fk_usuario_trans` (`id_usuario`),
  KEY `fk_categoria_trans` (`id_categoria`),
  CONSTRAINT `fk_categoria_trans` FOREIGN KEY (`id_categoria`) REFERENCES `categorias` (`id_categoria`) ON DELETE CASCADE,
  CONSTRAINT `fk_usuario_trans` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla gestor_finanzas.transacciones: ~0 rows (aproximadamente)
DELETE FROM `transacciones`;

-- Volcando estructura para tabla gestor_finanzas.usuarios
CREATE TABLE IF NOT EXISTS `usuarios` (
  `id_usuario` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `apellido` varchar(255) NOT NULL,
  `fecha_registro` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla gestor_finanzas.usuarios: ~0 rows (aproximadamente)
DELETE FROM `usuarios`;

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
