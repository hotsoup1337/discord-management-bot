-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema MET11
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `MET11` ;

-- -----------------------------------------------------
-- Schema MET11
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `MET11` DEFAULT CHARACTER SET utf8 ;
USE `MET11` ;

-- -----------------------------------------------------
-- Table `MET11`.`discord_user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `MET11`.`discord_user` (
  `iddiscord_user` VARCHAR(45) NOT NULL,
  `username` VARCHAR(45) NOT NULL,
  `userdiscriminator` INT NOT NULL,
  PRIMARY KEY (`iddiscord_user`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `MET11`.`student`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `MET11`.`student` (
  `idstudent` INT NOT NULL,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  `discord_user_iddiscord_user` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idstudent`),
  INDEX `fk_student_discord_user1_idx` (`discord_user_iddiscord_user` ASC),
  CONSTRAINT `fk_student_discord_user1`
    FOREIGN KEY (`discord_user_iddiscord_user`)
    REFERENCES `MET11`.`discord_user` (`iddiscord_user`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `MET11`.`teacher`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `MET11`.`teacher` (
  `idteacher` INT NOT NULL,
  `form_of_address` VARCHAR(45) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idteacher`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `MET11`.`lesson`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `MET11`.`lesson` (
  `idlesson` INT NOT NULL,
  `teacher_idteacher` INT NOT NULL,
  `lesson_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idlesson`),
  INDEX `fk_lesson_teacher1_idx` (`teacher_idteacher` ASC),
  CONSTRAINT `fk_lesson_teacher1`
    FOREIGN KEY (`teacher_idteacher`)
    REFERENCES `MET11`.`teacher` (`idteacher`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `MET11`.`student_has_lesson`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `MET11`.`student_has_lesson` (
  `student_idstudent` INT NOT NULL,
  `lesson_idlesson` INT NOT NULL,
  `grade` INT NOT NULL,
  PRIMARY KEY (`student_idstudent`, `lesson_idlesson`),
  INDEX `fk_student_has_lesson_lesson1_idx` (`lesson_idlesson` ASC),
  INDEX `fk_student_has_lesson_student_idx` (`student_idstudent` ASC),
  CONSTRAINT `fk_student_has_lesson_student`
    FOREIGN KEY (`student_idstudent`)
    REFERENCES `MET11`.`student` (`idstudent`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_student_has_lesson_lesson1`
    FOREIGN KEY (`lesson_idlesson`)
    REFERENCES `MET11`.`lesson` (`idlesson`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
